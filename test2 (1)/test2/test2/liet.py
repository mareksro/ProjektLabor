import os
import secrets
from datetime import datetime, timezone

import requests
from flask import Blueprint, jsonify, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# SQLAlchemy
db = SQLAlchemy()

user_bp = Blueprint("user", __name__)

map_bp = Blueprint("map", __name__)


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    secret_key = db.Column(db.Text, nullable=False)
    

    def __init__(self, username, password, secret_key=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.secret_key = secret_key or secrets.token_hex(24)

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  #adreses pievienošanas laiks, lai varētu veidot pareizus maršrutus

    def __init__(self, address, latitude, longitude):
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(255), nullable=False)
    addresses = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="pending", nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __init__(self, driver_name, addresses):
        self.driver_name = driver_name
        self.addresses = addresses


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return jsonify({"error": "Lietotājvārds un parole ir obligāts."}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Šāds lietotājs jau eksistē."}), 400

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Lietotājs veiksmīgi reģistrēts.", "secret_key": new_user.secret_key}), 201

    return render_template("register.html")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user"] = user.username
            session["secret_key"] = user.secret_key
            return jsonify({"message": "Pierakstīšanās veiksmīga."}), 200

        return jsonify({"error": "Nederīgs lietotājvārds vai parole."}), 401

    return render_template("login.html")


@user_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("secret_key", None)
    return jsonify({"message": "Līdz nākamajai reizei."}), 200


@user_bp.route("/profile")
def profile():
    if "user" in session:
        return jsonify({"message": f"Sveiks, {session['user']}! Tava slepenā atslēga: {session['secret_key']}"}), 200
    return jsonify({"error": "Unauthorized access."}), 401


@map_bp.route("/add_address", methods=["POST"])
def add_address():
    address = request.form.get("address")
    api_key = os.getenv("API_KEY")

    if not address:
        return jsonify({"error": "Adrese ir obligāta"}), 400

    # Google Address Validation API
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK" and data["results"]:
                location = data["results"][0]["geometry"]["location"]
                latitude, longitude = location["lat"], location["lng"]

                # Save to database
                new_location = Address(address=address, latitude=latitude, longitude=longitude)
                db.session.add(new_location)
                db.session.commit()

                return jsonify({"message": "Adrese veiksmīgi pievienota!"}), 201
    except requests.RequestException as e:
        return jsonify({"error": f"Nevarēja atrast ģeolokāciju: {e}"}), 500

    return jsonify({"error": "Nederīga adrese"}), 400