import json
import hashlib
import os

class UserManager:
    def __init__(self, users_file="pos_app/data/users.json"):
        self.users_file = users_file
        self.users = self.load_users()
        self._ensure_default_admin()

    def load_users(self):
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def _hash_password(self, password, salt):
        return hashlib.sha256(password.encode() + salt).hexdigest()

    def _ensure_default_admin(self):
        if not any(u['username'] == 'admin' for u in self.users):
            salt = os.urandom(16)
            password_hash = self._hash_password("admin", salt)
            self.users.append({
                "username": "admin",
                "password_hash": password_hash,
                "salt": salt.hex(),
                "role": "Admin"
            })
            self.save_users()
        # This part is to update the placeholder password in the initial users.json
        for user in self.users:
            if user['username'] == 'admin' and user['salt'] == 'a1b2c3d4e5f6':
                salt = os.urandom(16)
                password_hash = self._hash_password("admin", salt)
                user['salt'] = salt.hex()
                user['password_hash'] = password_hash
                self.save_users()
                break

    def verify_user(self, username, password):
        for user in self.users:
            if user["username"] == username:
                salt = bytes.fromhex(user["salt"])
                password_hash = self._hash_password(password, salt)
                if password_hash == user["password_hash"]:
                    return user["role"]
        return None
