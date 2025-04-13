from datetime import datetime

class Event:
    @staticmethod
    def create_event(data):
        return {
            "name": data["name"],
            "date": data.get("date", str(datetime.utcnow())),
            "location": data.get("location", ""),
            "description": data.get("description", ""),
            "image": data.get("image", ""),
            "category": data.get("category", ""),
            "popularity": data.get("popularity", 0)
        }

    @staticmethod
    def to_dict(event):
        return {
            "id": str(event["_id"]),
            "name": event["name"],
            "date": event["date"],
            "location": event["location"],
            "description": event["description"],
            "image": event.get("image", ""),
            "category": event.get("category", ""),
            "popularity": event.get("popularity", 0)
        }
