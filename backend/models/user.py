import bcrypt

class User:
    @staticmethod
    def hash_password(password):
        # Use bcrypt for secure password hashing
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')  # Store as string in the database

    @staticmethod
    def check_password(user, password):
        # Re-encode the stored hashed password (string) to bytes before verification
        return bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8'))

    @staticmethod
    def create_user(data):
        required_fields = ["username", "email", "password"]
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required fields: username, email, password")

        return {
            "username": data["username"],
            "email": data["email"],
            "password": User.hash_password(data["password"]),
            "bio": data.get("bio", ""),
            "profile_url": data.get("profile_url", "https://avatar.iran.liara.run/public/36")
        }

    @staticmethod
    def to_dict(user):
        return {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "bio": user.get("bio", "")
        }
