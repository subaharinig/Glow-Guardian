from flask import Blueprint, request, jsonify
from database import users_collection
import bcrypt
from bson import ObjectId
import datetime
import uuid

# =====================================
# CREATE BLUEPRINT
# =====================================

auth = Blueprint("auth", __name__)


# =====================================
# HELPER FUNCTION
# =====================================

def generate_token():
    """Generate simple session token"""
    return str(uuid.uuid4())


# =====================================
# REGISTER USER
# =====================================

@auth.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        # Validate input
        if not name or not email or not password:
            return jsonify({
                "success": False,
                "error": "All fields are required"
            }), 400

        # Check existing user
        if users_collection.find_one({"email": email}):
            return jsonify({
                "success": False,
                "error": "User already exists"
            }), 400

        # Hash password
        hashed_pw = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        # Save user
        user_id = users_collection.insert_one({
            "name": name,
            "email": email,
            "password": hashed_pw,
            "created_at": datetime.datetime.utcnow()
        }).inserted_id

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "user_id": str(user_id)
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =====================================
# LOGIN USER
# =====================================

@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "success": False,
                "error": "Email and password required"
            }), 400

        # Find user
        user = users_collection.find_one({"email": email})

        if not user:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404

        # Verify password
        if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return jsonify({
                "success": False,
                "error": "Invalid password"
            }), 401

        # Generate session token
        token = generate_token()

        # Save token in DB
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"session_token": token}}
        )

        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =====================================
# GET USER PROFILE (Protected Route)
# =====================================

@auth.route("/profile", methods=["GET"])
def profile():

    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    user = users_collection.find_one({"session_token": token})

    if not user:
        return jsonify({"error": "Invalid token"}), 401

    return jsonify({
        "name": user["name"],
        "email": user["email"]
    })
