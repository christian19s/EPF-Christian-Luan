import datetime
import json
import sqlite3
from contextlib import closing

from bottle import Bottle

from data import get_db_connection
from models.user import AuthUser, PermissionSystem

from .exceptions import AuthenticationFailed, UserNotFound

user_routes = Bottle()


class DuplicateUserError(Exception):
    pass


class UserService:
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user credentials"""
        user = UserService.get_user_by_username(username)
        if not user:
            raise UserNotFound(f"No user with username {username}")

        if not user.verify_password(password):
            raise AuthenticationFailed("Invalid password")
        return user

    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve user by ID"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()

        if not user_data:
            return None

        return UserService._hydrate_user(user_data)

    @staticmethod
    def _hydrate_user(user_data):
        """Create AuthUser instance from database row"""
        return AuthUser(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            password_hash=user_data["password_hash"],
            birthdate=user_data["birthdate"],
            profile_picture=user_data["profile_picture"],
            global_role=user_data["global_role"],
            created_at=user_data["created_at"],
            last_login=user_data["last_login"],
            wiki_roles=json.loads(user_data["wiki_roles"] or "{}"),
        )

    @staticmethod
    def get_user_by_email(email):
        return AuthUser.get_user_by_email(email)

    def user_can_create_wiki(self, user):
        """Check if user has permission to create wikis"""
        if not user:
            return False
        return PermissionSystem.can(user, PermissionSystem.CREATE_WIKI)

    @staticmethod
    def get_user_by_username(username):
        """Retrieve user by username"""
        return AuthUser.get_user_by_username(username)

    @staticmethod
    def update_user_profile(user_id, **updates):
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values())
            values.append(user_id)

            cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
            conn.commit()

        return UserService.get_user_by_id(user_id)

    @staticmethod
    def change_password(user_id, current_password, new_password):
        """Change user password with validation"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise UserNotFound(f"User ID {user_id} not found")

        if not user.verify_password(current_password):
            raise AuthenticationFailed("Current password is incorrect")

        user.change_password(new_password)
        return user

    @staticmethod
    def _get_all_users():
        """Retrieve all users from the database"""
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users_data = cursor.fetchall()

        users = []
        for user_data in users_data:
            users.append(
                AuthUser(
                    id=user_data["id"],
                    username=user_data["username"],
                    email=user_data["email"],
                    password_hash=user_data["password_hash"],
                    birthdate=user_data["birthdate"],
                    profile_picture=user_data["profile_picture"],
                    global_role=user_data["global_role"],  # Changed from permissions
                    created_at=user_data["created_at"],
                    last_login=user_data["last_login"],
                    wiki_roles=json.loads(user_data["wiki_roles"] or "{}"),
                )
            )
        return users

    @staticmethod
    def delete_user(user_id):
        """Delete a user from the database"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

    @staticmethod
    def get_all_users():
        """Public method to get all users"""
        return UserService._get_all_users()
