import requests
from flask import Flask, render_template, request, jsonify
import folium
import os
import itertools
import polyline  # Install this with `pip install polyline`

app = Flask(__name__)

# Define cities and their coordinates (corrected coordinates)
cities = {
    "Riga": (56.9496, 24.1052),
    "Jelgava": (56.6527, 23.7129),
    "Daugavpils": (55.8714, 26.5168),
    "Liepaja": (56.5078, 21.0138),
    "Valmiera": (57.5411, 25.4245),
    "Alūksne": (57.4242, 27.0467),
    "Tukums": (56.9677, 23.1557),
    "Kuldīga": (56.9671, 21.9686),
    "Ventspils": (57.4088, 21.6206),
    "Madona": (56.8542, 26.2189),
    "Kandava": (57.0341, 22.7801),
    "Saldus": (56.6635, 22.4886),
    "Aizkraukle": (56.6047, 25.2546),
    "Cēsis": (57.3119, 25.2743),
    "Ogre": (56.8165, 24.6050),
    "Jēkabpils": (56.4926, 25.8666),
    "Rēzekne": (56.5072, 27.3341),
    "Ludza": (56.5380, 27.7183),
    "Jūrmala": (56.9720, 23.8021),
    "Rūjiena": (57.8975, 25.3328),
    "Olaine": (56.7885, 23.9378)
}

MAX_HOURS = 7.5  # Maximum time for a single route in hours
MAX_ROUTES = 10  # Maximum number of concurrent routes

# Cache for API responses to reduce calls
POLYLINE_CACHE = {}

routes = []  # List to store unique routes

# Predefined colors for each route
ROUTE_COLORS = [
    "red", "blue", "green", "purple", "orange", "darkred", "lightblue", "darkgreen", "lightgray", "black"
]

def get_route_polyline_and_duration(api_key, start, end):
    """Fetch the polyline and duration data for the route between two locations."""
    if (start, end) in POLYLINE_CACHE:
        return POLYLINE_CACHE[(start, end)]

    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{cities[start][0]},{cities[start][1]}",
        "destination": f"{cities[end][0]},{cities[end][1]}",
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
                POLYLINE_CACHE[(start, end)] = (polyline_data, duration_seconds)
                return polyline_data, duration_seconds
    except requests.RequestException as e:
        print(f"Error fetching route polyline: {e}")
    return None, None

def generate_map_for_routes(routes, api_key):
    """Generate a Folium map with all routes, each route with a unique color."""
    if not routes:
        return None

    # Center the map on Riga
    route_map = folium.Map(location=cities["Riga"], zoom_start=7)

    for idx, route in enumerate(routes):
        color = ROUTE_COLORS[idx % len(ROUTE_COLORS)]  # Assign a color based on the index
        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            start_coords = cities[start]
            end_coords = cities[end]

            # Add markers for start and end cities
            folium.Marker(location=start_coords, popup=f"{start}").add_to(route_map)
            folium.Marker(location=end_coords, popup=f"{end}").add_to(route_map)

            # Fetch the route polyline from the API
            polyline_data, _ = get_route_polyline_and_duration(api_key, start, end)
            if polyline_data:
                # Decode polyline and add it to the map
                decoded_points = polyline.decode(polyline_data)
                folium.PolyLine(decoded_points, color=color, weight=2.5).add_to(route_map)

    return route_map

def generate_routes_with_max_cities(api_key):
    """Generate routes ensuring one driver covers as many cities as possible within 7 hours."""
    global routes
    routes = []  # Reset routes

    other_cities = [city for city in cities if city != "Riga"]

    while other_cities:
        temp_route = ["Riga"]
        total_duration = 0
        current_city = "Riga"

        while True:
            nearest_city = None
            shortest_duration = float("inf")

            # Find the nearest city that can be added to the route
            for city in other_cities:
                _, duration_to_next = get_route_polyline_and_duration(api_key, current_city, city)
                _, duration_to_riga = get_route_polyline_and_duration(api_key, city, "Riga")
                if duration_to_next and duration_to_riga:
                    if total_duration + duration_to_next + duration_to_riga <= MAX_HOURS * 3600 and duration_to_next < shortest_duration:
                        nearest_city = city
                        shortest_duration = duration_to_next

            if nearest_city:
                temp_route.append(nearest_city)
                total_duration += shortest_duration
                other_cities.remove(nearest_city)
                current_city = nearest_city
            else:
                break

        # Complete the route by returning to Riga
        temp_route.append("Riga")
        _, duration_to_riga = get_route_polyline_and_duration(api_key, current_city, "Riga")
        if duration_to_riga:
            total_duration += duration_to_riga

        routes.append((temp_route, total_duration))

@app.route("/")
def home():
    """Home page with instructions."""
    return """
    <h1>Welcome to the Circular Routes App</h1>
    <p>Use the following endpoints:</p>
    <ul>
        <li><a href="/map">/map</a> - View the map of circular routes.</li>
        <li><a href="/generate">/generate</a> - Generate routes automatically.</li>
        <li><a href="/routes">/routes</a> - Manage routes.</li>
    </ul>
    """

@app.route("/map")
def display_map():
    """Display the map with the calculated routes."""
    api_key = os.getenv("API_KEY")  # Ensure you set this environment variable
    if not routes:
        return "<h1>No routes defined. Please generate routes first.</h1>"

    # Generate a map with all routes
    route_map = generate_map_for_routes([route[0] for route in routes], api_key)
    if not route_map:
        return "<h1>Unable to generate map.</h1>"

    # Generate the text description of routes
    route_descriptions = """<h2>Driver Routes</h2><ul>"""
    for idx, (route, duration) in enumerate(routes):
        formatted_duration = f"{int(duration // 3600)} hours {int((duration % 3600) // 60)} minutes"
        route_descriptions += f"<li>Driver {idx + 1}: {' -> '.join(route)} (Total time: {formatted_duration})</li>"
    route_descriptions += "</ul>"

    map_html = route_map._repr_html_()
    return f"<h1>Route Map</h1>{map_html}{route_descriptions}"

@app.route("/generate")
def generate():
    """Generate routes automatically."""
    api_key = os.getenv("API_KEY")
    generate_routes_with_max_cities(api_key)
    return jsonify({"message": "Routes generated successfully.", "routes": [route[0] for route in routes]}), 200

@app.route("/routes", methods=["GET", "POST", "DELETE"])
def manage_routes():
    """CRUD operations for managing routes."""
    global routes

    if request.method == "GET":
        return jsonify({"routes": [route[0] for route in routes]}), 200

    elif request.method == "POST":
        if len(routes) >= MAX_ROUTES:
            return jsonify({"error": f"Cannot add more than {MAX_ROUTES} routes."}), 400

        data = request.get_json()
        new_route = data.get("route")

        if new_route and all(city in cities for city in new_route):
            if new_route[0] != "Riga" or new_route[-1] != "Riga":
                return jsonify({"error": "Each route must start and end in Riga."}), 400

            # Calculate total duration for the route
            api_key = os.getenv("API_KEY")
            total_duration = 0
            for i in range(len(new_route) - 1):
                _, duration = get_route_polyline_and_duration(api_key, new_route[i], new_route[i + 1])
                if duration:
                    total_duration += duration

            if total_duration / 3600 <= MAX_HOURS:
                routes.append((new_route, total_duration))
                return jsonify({"message": "Route added successfully.", "route": new_route}), 201
            else:
                return jsonify({"error": "Route exceeds maximum allowed time of 7 hours."}), 400
        else:
            return jsonify({"error": "Invalid route. Ensure all cities exist."}), 400

    elif request.method == "DELETE":
        data = request.get_json()
        route_to_delete = data.get("route")

        for route in routes:
            if route[0] == route_to_delete:
                routes.remove(route)
                return jsonify({"message": "Route deleted successfully.", "route": route_to_delete}), 200

        return jsonify({"error": "Route not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)
