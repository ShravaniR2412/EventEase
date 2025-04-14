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
            "time": data.get("time", ""),  # lowercase 'time' for consistency
            "created_by": data.get("created_by")
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
            "time": event.get("time", ""),  # include time in dict
            "popularity": event.get("popularity", 0),
            "created_by": str(event.get("created_by", ""))
        }
