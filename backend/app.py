from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
