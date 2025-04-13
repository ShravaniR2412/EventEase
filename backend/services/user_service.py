from bson.objectid import ObjectId
from models.user import User

class UserService:
    def __init__(self, mongo):
        self.mongo = mongo

    def register_user(self, data):
        user_data = User.create_user(data)
        self.mongo.db.users.insert_one(user_data)
        return user_data

    def login_user(self, data):
        user = self.mongo.db.users.find_one({"username": data["username"]})
        if user and User.check_password(user, data["password"]):
            return User.to_dict(user)
        return None
    
    def update_user(self, user_id, data):
        self.mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})
        user = self.mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User.to_dict(user)
