import json
import os
from contextlib import closing

from bottle import Bottle

from db import get_db_connection
from models.auth_user import AuthUser, generate_password_hash, verify_password

user_routes = Bottle()


class UserService:
    def get_all(self):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = []
            for row in cursor.fetchall():
                # Convert sqlite3.Row to dictionary
                user_data = dict(row)
                # Convert JSON string to dict for wiki_roles
                if user_data.get("wiki_roles"):
                    user_data["wiki_roles"] = json.loads(user_data["wiki_roles"])
                users.append(AuthUser(**user_data))
            return users

    def get_by_id(self, user_id):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                return None
            user_data = dict(row)
            # Convert JSON string to dict for wiki_roles
            if user_data.get("wiki_roles"):
                user_data["wiki_roles"] = json.loads(user_data["wiki_roles"])
            return AuthUser(**user_data)

    def create_user(
        self, username, email, password, birthdate=None, profile_picture=None
    ):
        # Generate password hash
        password_hash = generate_password_hash(password)

        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO users 
                (username, email, password_hash, birthdate, profile_picture, wiki_roles) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    username,
                    email,
                    password_hash,
                    birthdate,
                    profile_picture,
                    json.dumps({}),
                ),
            )
            conn.commit()

    def update_user(
        self,
        user_id,
        username,
        email,
        password=None,
        birthdate=None,
        profile_picture=None,
    ):
        user = self.get_by_id(user_id)
        if not user:
            return False

        # Prepare update fields
        updates = {
            "username": username,
            "email": email,
            "birthdate": birthdate,
            "profile_picture": profile_picture,
        }

        # Update password if provided
        if password:
            user.change_password(password)
            updates["password_hash"] = user.password_hash

        # Update other fields
        user.update_profile(**updates)
        return True

    def delete_user(self, user_id):
        user = self.get_by_id(user_id)
        if not user:
            return False

        # Delete profile picture if exists
        if user.profile_picture:
            try:
                profile_path = os.path.join(UPLOAD_DIR, user.profile_picture)
                if os.path.exists(profile_path):
                    os.remove(profile_path)
            except OSError:
                pass  # Log error in production

        # Delete from database
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
        return True
