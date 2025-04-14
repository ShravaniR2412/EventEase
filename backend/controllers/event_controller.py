from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from models.event import Event
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

# Retrieve MongoDB URI from environment variable
uri = os.getenv("MONGO_URI")
if not uri:
    raise RuntimeError("MONGO_URI environment variable is not set")

# Initialize MongoClient
client = MongoClient(uri)

event_blueprint = Blueprint('event', __name__)

# Create an event
@event_blueprint.route("/create", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    try:
        event_data = Event.create_event(data)
        result = client["events_db"]["events"].insert_one(event_data)
        event_data["_id"] = str(result.inserted_id)
        return jsonify(Event.to_dict(event_data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Read all events
@event_blueprint.route("/get", methods=["GET"])
def get_all_events():
    try:
        # Assuming user_id is passed as a query parameter
        user_id = request.args.get('user_id')  # Example: /get?user_id=123
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        # Find all events where the 'created_by' field matches the user_id
        events_cursor = client["events_db"]["events"].find({"created_by": user_id})
        
        # Convert MongoDB documents to dictionaries using the Event model
        events = [Event.to_dict(event) for event in events_cursor]
        
        return jsonify(events), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Read a single event
@event_blueprint.route("/get/<string:event_id>", methods=["GET"])
def get_event(event_id):
    try:
        object_id = ObjectId(event_id)
        event = client["events_db"]["events"].find_one({"_id": object_id})
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify(Event.to_dict(event)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update an event using POST
@event_blueprint.route("/update/<string:event_id>", methods=["POST"])
def update_event(event_id):
    data = request.get_json()

    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    try:
        object_id = ObjectId(event_id)
        result = client["events_db"]["events"].update_one(
            {"_id": object_id},
            {"$set": data}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Event not found"}), 404

        updated_event = client["events_db"]["events"].find_one({"_id": object_id})
        return jsonify(Event.to_dict(updated_event)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete an event
@event_blueprint.route("/delete/<string:event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        object_id = ObjectId(event_id)
        result = client["events_db"]["events"].delete_one({"_id": object_id})
        if result.deleted_count == 0:
            return jsonify({"error": "Event not found"}), 404
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
