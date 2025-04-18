from flask import Flask,Blueprint, request, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from otp import generate_and_send_otp, get_stored_otp
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Set Mongo URI from environment variable
MONGO_URI = os.getenv('MONGO_URI')
print("Mongo URI:", MONGO_URI)
app.config["MONGO_URI"] = MONGO_URI

# Initialize PyMongo
mongo = PyMongo(app)

# Test MongoDB connection
try:
    mongo.cx.admin.command("ping")
    print("Connected to MongoDB successfully!")
except Exception as e:
    raise RuntimeError(f"Failed to initialize database connection: {e}")

# Register blueprints after Mongo is initialized (to avoid circular import)
from controllers.event_controller import event_blueprint
from controllers.user_controller import user_blueprint

# Inject mongo into blueprints if needed (optional)
app.register_blueprint(event_blueprint, url_prefix="/events")
app.register_blueprint(user_blueprint, url_prefix="/users")

@app.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    result = generate_and_send_otp(email)
    if result["success"]:
        return jsonify({"message": "OTP sent"})
    return jsonify({"error": result["error"]}), 500

@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp_entered = data.get("otp")

    if not email or not otp_entered:
        return jsonify({"error": "Email and OTP required"}), 400

    otp_actual = get_stored_otp(email)
    if otp_actual == otp_entered:
        return jsonify({"message": "OTP verified!"})
    return jsonify({"error": "Invalid OTP"}), 401


if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     email = "shravanirasam0212@gmail.com"
#     result = generate_and_send_otp(email)
#     print(result)
