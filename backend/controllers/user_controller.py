from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from services.user_service import UserService
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

# Retrieve MongoDB URI from environment variable
uri = os.getenv("MONGO_URI")
if not uri:
    raise RuntimeError("MONGO_URI environment variable is not set")

# Initialize MongoClient
client = MongoClient(uri)

user_blueprint = Blueprint('user', __name__)

# Helper function to serialize ObjectId to string
def serialize_document(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# Register a user
@user_blueprint.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    try:
        user = UserService(client).register_user(data)
        return jsonify(serialize_document(user)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Login a user
@user_blueprint.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    try:
        user = UserService(client).login_user(data)
        if user:
            return jsonify(serialize_document(user)), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a user
@user_blueprint.route("/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    try:
        object_id = ObjectId(user_id)
        updated_user = UserService(client).update_user(str(object_id), data)
        return jsonify(serialize_document(updated_user)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
