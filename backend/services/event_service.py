from bson.objectid import ObjectId
from models.event import Event

class EventService:
    def __init__(self, mongo):
        self.mongo = mongo

    def create_event(self, data):
        # Validate and create the event object using the Event model
        event_data = Event.create_event(data)
        
        # Insert the new event into MongoDB
        result = self.mongo.db.events.insert_one(event_data)
        
        # Add the generated ID to the response object
        event_data["_id"] = str(result.inserted_id)
        
        return Event.to_dict(event_data)

    def get_all_events(self, user_id):
        # Find all events where the 'created_by' field matches the user_id
        events_cursor = self.mongo.db.events.find({"created_by": user_id})
        
        # Convert MongoDB documents to dictionaries using the Event model
        events = [Event.to_dict(event) for event in events_cursor]
        
        return events

    def get_event_by_id(self, event_id):
        try:
            # Convert string ID to ObjectId for querying MongoDB
            object_id = ObjectId(event_id)
            event = self.mongo.db.events.find_one({"_id": object_id})
            return Event.to_dict(event) if event else None
        except Exception as e:
            raise Exception("Invalid ID format")

    def update_event(self, event_id, data):
        try:
            object_id = ObjectId(event_id)
            
            # Perform the update operation in MongoDB
            result = self.mongo.db.events.update_one(
                {"_id": object_id},
                {"$set": data}
            )
            
            if result.matched_count == 0:
                return None
            
            # Fetch and return the updated document
            updated_event = self.mongo.db.events.find_one({"_id": object_id})
            return Event.to_dict(updated_event)
        
        except Exception as e:
            raise Exception("Failed to update the event: " + str(e))

    def delete_event(self, event_id):
        try:
            object_id = ObjectId(event_id)
            
            # Perform the delete operation in MongoDB
            result = self.mongo.db.events.delete_one({"_id": object_id})
            
            # Return True if deletion was successful, False otherwise
            return result.deleted_count > 0
        
        except Exception as e:
            raise Exception("Failed to delete the event: " + str(e))
