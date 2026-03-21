from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from models import db, User

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400
    if len(data["username"]) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"error": "Username already taken"}), 409
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(username=data["username"], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Account created", "username": user.username}), 201
