import os
from datetime import datetime, time, timezone
import folium
import geopy.distance  # pip install geopy
import polyline  # Instalet so var ar `pip install polyline`
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from sqlalchemy import text

from liet import Address  # importee lietotaja datus un datubazi no list.py
from liet import Route, db, map_bp, user_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_default_key")

# SQLAlchemy konfiguracija
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# nepieciesams, lai uzsaktu darbibu ar aplikaciju
db.init_app(app)

# Tiek registrets blueprints prieks lietotaju marsrutiem
app.register_blueprint(map_bp, url_prefix="/map")
app.register_blueprint(user_bp)


MAX_HOURS = 7.5  # Maksimalais viena marsruta ilgums
MAX_ROUTES = 10  # Maksimalais vienlaicigu marsrutu skaits (pienemam, ka mums ir 10 kurjeri)

# API kešatmiņa lai samazinatu calls
POLYLINE_CACHE = {}
routes = []  # Saraksts unikālu marsrutu glabasanai

# Marsrutu krasas
ROUTE_COLORS = ["red", "blue", "green", "purple", "orange", "darkred", "pink", "darkgreen", "brown", "black"]

def get_route_polyline_and_duration(api_key, start_coords, end_coords):
    """Fetch the polyline and duration data for the route between two locations."""
    if (start_coords, end_coords) in POLYLINE_CACHE:
        return POLYLINE_CACHE[(start_coords, end_coords)]

    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{start_coords[0]},{start_coords[1]}",
        "destination": f"{end_coords[0]},{end_coords[1]}",
        "key": api_key,
        "mode": "driving"
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK" and "routes" in data and data["routes"]:
                polyline_data = data["routes"][0]["overview_polyline"]["points"]
                duration_seconds = data["routes"][0]["legs"][0]["duration"]["value"]
                POLYLINE_CACHE[(start_coords, end_coords)] = (polyline_data, duration_seconds)
                return polyline_data, duration_seconds
    except requests.RequestException as e:
        print(f"Error fetching route polyline: {e}")
    return None, None

def is_near_polyline(polyline_points, city_coords, threshold_km=20):
    """Check if a city is near a polyline within a certain threshold."""
    for point in polyline_points:
        distance = geopy.distance.distance((point[0], point[1]), city_coords).km
        if distance <= threshold_km:
            return True
    return False

def generate_map_for_routes(routes,api_key):
    """Generate a Folium map with all routes, each route with a unique color."""
    if not routes:
        return None

    # Center the map on Riga
    route_map = folium.Map(location=(56.9496, 24.1052), zoom_start=7)

    for idx, route in enumerate(routes):
        color = ROUTE_COLORS[idx % len(ROUTE_COLORS)]  # Pieskir marsrutam krasinu
        for i, coords in enumerate(route):
            # Markieru pievienosana
            if i == len(route) - 1:
                folium.Marker(
                    location=coords,
                    popup="Noliktava",
                    tooltip="Noliktava",
                    icon=folium.Icon(color="red", icon="home")
                ).add_to(route_map)
            else:
                # Adresu nosauksana
                folium.Marker(
                    location=coords,
                    popup=f"Adrese Nr. {i}",
                    tooltip=f"Adrese Nr. {i}",
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(route_map)

            # Marsruta uzzimesana kartee
            if i < len(route) - 1:
                start_coords = coords
                end_coords = route[i + 1]

                # Iegust attelojamo marsrutu ar API
                polyline_data, _ = get_route_polyline_and_duration(api_key, start_coords, end_coords)
                if polyline_data:
                    # Marsruta dekodesana un taa pievienosana kartei
                    decoded_points = polyline.decode(polyline_data)
                    folium.PolyLine(decoded_points, color=color, weight=2.5).add_to(route_map)

       
    return route_map

def generate_routes_with_max_cities(api_key):
    """Generate routes ensuring one driver covers as many cities as possible within 7 hours."""
    global routes
    routes = []

    # Nepieciesams, lai identificetu tadus laikus kaa plkst 00:00
    now = datetime.now(timezone.utc)
    cutoff_time = datetime.combine(now.date(), time(22, 0), tzinfo=timezone.utc)

    all_addresses = Address.query.filter(Address.created_at < cutoff_time).all()
    remaining_cities = [(addr.id, (addr.latitude, addr.longitude)) for addr in all_addresses]
    starting_coords = (56.9496, 24.1052)  # Riga coordinates

    while remaining_cities:
        temp_route = [starting_coords]
        total_duration = 0
        current_coords = starting_coords
        used_address_ids = []

        while True:
            nearest_city = None
            shortest_duration = float("inf")
            intermediate_cities = []

            # Find the nearest city
            for city in remaining_cities:
                city_id, (latitude, longitude) = city
                polyline_data, duration_to_next = get_route_polyline_and_duration(api_key, current_coords, (latitude, longitude))
                _, duration_to_riga = get_route_polyline_and_duration(api_key, (latitude, longitude), starting_coords)

                if duration_to_next and duration_to_riga:
                    if total_duration + duration_to_next + duration_to_riga <= MAX_HOURS * 3600:
                        # Check for intermediate cities
                        if polyline_data:
                            decoded_points = polyline.decode(polyline_data)
                            for other_city in remaining_cities:
                                if other_city != city and is_near_polyline(decoded_points, other_city[1]):
                                    intermediate_cities.append(other_city)

                        # Atrod tuvako adresi un vismazako laiku:
                        if duration_to_next < shortest_duration:
                            nearest_city = city
                            shortest_duration = duration_to_next

            if nearest_city:# Pievieno pilsetu marsrutam:
                city_id, (latitude, longitude) = nearest_city
                temp_route.append((latitude, longitude))
                total_duration += shortest_duration
                remaining_cities.remove(nearest_city)
                used_address_ids.append(city_id)

                for inter_city in intermediate_cities:
                    inter_id, (inter_lat, inter_lon) = inter_city
                    if inter_city in remaining_cities:
                        temp_route.append((inter_lat, inter_lon))
                        remaining_cities.remove(inter_city)
                        used_address_ids.append(inter_id)

                current_coords = (latitude, longitude)
            else:
                break

        # Pabeidz marsrutu Rigaa
        _, duration_to_riga = get_route_polyline_and_duration(api_key, current_coords, starting_coords)
        if duration_to_riga:
            total_duration += duration_to_riga
        temp_route.append(starting_coords)

        # Marsruts tiek saglabats
        routes.append((temp_route, total_duration))

        # Tiek saglabats datubazee "pending" statusaa
        route = Route(driver_name=f"Driver {len(routes)}", addresses=",".join(map(str, used_address_ids)))
        db.session.add(route)

    db.session.commit()


@app.route("/") # sakumlapa
def home():
    """Home page with instructions."""
    return """
    <link rel="stylesheet" href="static/css/dizains.css">
    <body>
    <style>
        body {
             background: url('static/images/lv.png') no-repeat bottom right;
             background-width: auto 50%;
        }
    </style>
        <div id="reg">
            <a href="/register">Reģistrēties</a>
            <a href="/login">Ienākt</a><br>
        </div>
            <image src="static/images/p1.png" style="width:10%; padding:4%;"><br>
            <a href="/map">Apskatīt karti</a>
            <a href="/generate">Ģenerēt maršrutus</a>
            <a href="/add_address">Pievienot adresi</a>
            <a href="/approve_routes">Apstiprināt</a><br>
            <br><br>
            <br><br>
            <a id="clearButton">Notīrīt visus maršrutus</a>
            <p id="clearMessage"></p>

            <script>
                document.getElementById("clearButton").addEventListener("click", async function() {
                    const response = await fetch('/clear_addresses', { method: 'POST' });
                    const data = await response.json();
                    document.getElementById("clearMessage").textContent = data.message || data.error;
                });
            </script>
    </body>
            
    """

@app.route("/approve_routes", methods=["GET", "POST"])#Marsrutu apstiprinasana
def approve_routes():
    """Maršrutu apstiprināšana."""
    
    if request.method == "POST":
        # 
        approved_routes_ids= request.form.getlist("approved_route_ids")
        complete_routes_ids = request.form.getlist("complete_route_ids")
        
        # Tiek apstradati apstiprinajumi
        for route_id in approved_routes_ids:
            route = Route.query.get(route_id)
            if route and route.status != "approved":
                route.status = "approved"

        # Pabeidz un izdzes izveletos marsrutus
        for route_id in complete_routes_ids:
            route = Route.query.get(route_id)
            if route:
                # Izdzes saistitas adreses:
                address_ids = list(map(int, route.addresses.split(",")))
                Address.query.filter(Address.id.in_(address_ids)).delete(synchronize_session=False)

                # Izdzes marsrutus
                db.session.delete(route)

        # Saglaba izmainas datubazee
        db.session.commit()


    
    pending_routes = Route.query.filter(Route.status=="pending").all()
    approved_routes = Route.query.filter(Route.status=="approved").all()

    # Render a simple HTML form with checkboxes for approval and completion
    return render_template("approve_routes.html", pending_routes=pending_routes, approved_routes=approved_routes)


@app.route("/generate")
def generate():
    """Automātiski ģenerēti maršruti."""
    api_key = os.getenv("API_KEY")

    now = datetime.now(timezone.utc)
    cutoff_time = datetime.combine(now.date(), time(22, 0), tzinfo=timezone.utc)

    # Iekļūšt gaidīšanas sarakstā pēc plkst 00:00
    waiting_addresses = Address.query.filter(Address.created_at >= cutoff_time).all()
    waiting_count = len(waiting_addresses)

    # Lai iegūtu adreses neapstiprinātajiem maršrutiem:
    unapproved_routes = Route.query.filter_by(status="pending").all()
    unapproved_address_ids = set(
        int(addr_id) for route in unapproved_routes for addr_id in route.addresses.split(",")
    )

    # Vel neiekļautās adreses tiek pievienotas nākamajam maršrutam
    generate_routes_with_max_cities(api_key)

    return jsonify({
        "message": "Maršruti veiksmīgi ģenerēti.",
        "routes": [route[0] for route in routes],
        "waiting_addresses": waiting_count,
        "unapproved_routes": len(unapproved_routes),
        "note": "Iepriekš neizpildīti maršruti tagad tiks veikti."
    }), 200

@app.route("/map/<int:route_id>", methods=["GET"])
@app.route("/map", methods=["GET"])
def display_map(route_id=None):
    """Display the map with approved routes and their drivers."""
    api_key = os.getenv("API_KEY")  # API atstat!

    # Rīgas coords
    riga_coords = (56.9496, 24.1052)

    if route_id:
        # Sanem specifisku apstiprinatu marsrutu:
        route = Route.query.filter_by(id=route_id, status="approved").first()
        if not route:
            return f"<h1>Maršruts ar ID {route_id} nav apstiprināts vai neeksistē.</h1>", 404

        # Nakamais kodins ir lai iegutu koordinates prieks marsruta
        addresses = route.addresses.split(",")
        coords = [
            (Address.query.get(int(addr_id)).latitude, Address.query.get(int(addr_id)).longitude)
            for addr_id in addresses
        ]

        # Rīga - kā sākuma un beigu punkts
        route_details = [[riga_coords] + coords + [riga_coords]]
        drivers = [route.driver_name]
    else:
        # Salasam visus apstiprinatos marsrutus te
        approved_routes = Route.query.filter_by(status="approved").all()
        if not approved_routes:
            return "<h1>Nav maršrutu ko parādīt uz kartes.</h1>", 404

        # Te tiek sagatavoti visi iespejamie maršruti priekš nākamās kartes maršrutu ģenerēšanas
        route_details = []
        drivers = []
        for route in approved_routes:
            addresses = route.addresses.split(",")
            coords = [
                (Address.query.get(int(addr_id)).latitude, Address.query.get(int(addr_id)).longitude)
                for addr_id in addresses
            ]

            # Riga - sakums un beigas
            route_details.append([riga_coords] + coords + [riga_coords])
            drivers.append(route.driver_name)

    try:
        route_map = generate_map_for_routes(route_details, api_key)

        # Vajag aprekinat laiku marsruta izpildei:
        route_durations = []
        for route_coords in route_details:
            total_duration = 0
            for i in range(len(route_coords) - 1):
                start_coords = route_coords[i]
                end_coords = route_coords[i + 1]
                _, segment_duration = get_route_polyline_and_duration(api_key, start_coords, end_coords)
                if segment_duration:
                    total_duration += segment_duration
            route_durations.append(total_duration)

        route_descriptions = """<h2>Apstiprināti (Izpildītie) maršruti</h2><ul>"""
        for idx, (coords, duration) in enumerate(zip(route_details, route_durations)):
            formatted_duration = f"{int(duration // 3600)} stundas {int((duration % 3600) // 60)} minūtes"
            formatted_route = " -> ".join(f"({lat:.6f}, {lng:.6f})" for lat, lng in coords)
            route_descriptions += f"<li>Driver: {drivers[idx]}, Route: {formatted_route} (Kopējais laiks: {formatted_duration})</li>"
        route_descriptions += "</ul>"

        # Apvieno maršrutus un karti te:
        map_html = route_map._repr_html_()
        return f"<h1>Maršrutu karte</h1>{map_html}{route_descriptions}"
    except Exception as e:
        return f"<h1>Kļūda ģenerējot maršrutu: {e}</h1>"




@app.route("/add_address", methods=["GET","POST"])
def add_address():
    api_key = os.getenv("API_KEY")

    if request.method == "POST":
        address = request.form.get("address")

        if not address:
            return jsonify({"error": "Ir nepieciešama adrese"}), 400

    # Google Address Validation API
        base_url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "address": {
                "regionCode": "LV",
                "addressLines": [address]
        }
    }
        try:
            response = requests.post(base_url, json=payload, headers=headers)
            data = response.json()
            if response.status_code == 200 and "result" in data:
                geocode = data["result"].get("geocode", {}).get("location", {})
                if geocode:
                    latitude, longitude = geocode.get("latitude"), geocode.get("longitude")
                    if latitude is not None and longitude is not None:
                        # Saglabaa ieks db
                        new_location = Address(address=address, latitude=latitude, longitude=longitude)
                        db.session.add(new_location)
                        db.session.commit()

                        return jsonify({"message": "Adrese veiksmīgi pievienota"}), 201
            else:
                return jsonify({"error": "Nederīga adrese"}), 400
        except requests.RequestException as e:
            return jsonify({"error": f"Nevarēja atrast ģeolokāciju: {e}"}), 500

        return jsonify({"error": "Nederīga adrese"}), 400
    return """
    <body>
    <div style="padding-top:2%;">
    <a href="/">Atpakaļ</a>
    </div>
    <link rel="stylesheet" href="static/css/dizains.css">
    <div style="padding:5%;">
        <h1>Pievieno adresi</h1>
        <h4>Ievades laukā norādi Ielu, ielas numuru un pilsētu:</h4>
        <form method="POST" action="/add_address">
            <input type="text" placeholder="Adrese" name="address" required>
            <button type="submit">Pievienot</button>
        </form>
        </div>
        <style>
        body {
             background: url('static/images/lv.png') no-repeat bottom right;
             background-size: auto 50%;
        }
        </style>
    </body>
    """

@app.route("/clear_addresses", methods=["POST"])
def clear_addresses():
    try:
        # Delete all addresses from the database
        db.session.execute(text(f"TRUNCATE TABLE {Address.__tablename__} RESTART IDENTITY CASCADE;"))
        db.session.commit()
        return jsonify({"message": "All addresses have been cleared."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to clear addresses: {e}"}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Sis ir jaatstaj - parliecinas, vai db ir izveidota
        pass

    app.run(debug=True)


