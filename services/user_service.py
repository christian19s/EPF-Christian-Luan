import datetime
import json
import os
import sqlite3
from contextlib import closing

from bottle import Bottle
from data import get_db_connection
from models.user import AuthUser, generate_password_hash, verify_password

from .exceptions import AuthenticationFailed, DuplicateUser, UserNotFound

user_routes = Bottle()


class UserService:
    @staticmethod
    def create_user(username, email, password, birthdate=None, profile_picture=None):
        """Create a new user with validation"""
        # Check for existing user
        if UserService.get_user_by_email(email):
            raise DuplicateUser(f"Email {email} is already registered")
        if UserService.get_user_by_username(username):
            raise DuplicateUser(f"Username {username} is already taken")

        # Create and return new user
        return AuthUser.create_user(
            username=username,
            email=email,
            password=password,
            birthdate=birthdate,
            profile_picture=profile_picture,
        )

    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user credentials"""

        print(f"Authenticating user: {username}")

        user = UserService.get_user_by_username(username)
        if not user:
            raise UserNotFound(f"Nenhum usuario com o nome {username}")

        if not user.verify_password(password):
            raise AuthenticationFailed("Invalid password")
        print(f"Stored hash: {user.password_hash if user else 'No user found'}")
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
    def get_user_by_email(email):
        """Retrieve user by email"""
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user_data = cursor.fetchone()

        if not user_data:
            return None

        return UserService._hydrate_user(user_data)

    @staticmethod
    def get_user_by_username(username):
        """Retrieve user by username"""
        with closing(get_db_connection()) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
        return UserService._hydrate_user(user_data)

    @staticmethod
    def update_user_profile(user_id, **updates):
        """Update user profile information"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise UserNotFound(f"User ID {user_id} not found")
        if updates:
            user.update_profile(**updates)
        return user

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
    def _hydrate_user(user_data):
        return AuthUser(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            password_hash=user_data["password_hash"],
            birthdate=user_data["birthdate"],
            profile_picture=user_data["profile_picture"],
            role=user_data["permissions"],
            created_at=user_data["created_at"],
            last_login=user_data["last_login"],
            wiki_roles=json.loads(user_data["wiki_roles"] or "{}"),
        )

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
            # Parse JSON fields and convert to Python objects
            try:
                wiki_roles = (
                    json.loads(user_data["wiki_roles"])
                    if user_data["wiki_roles"]
                    else {}
                )
            except json.JSONDecodeError:
                wiki_roles = {}

            # Convert timestamp strings to datetime objects
            created_at = 0
            last_login = 0

            users.append(
                AuthUser(
                    id=user_data["id"],
                    username=user_data["username"],
                    email=user_data["email"],
                    password_hash=user_data["password_hash"],
                    birthdate=user_data["birthdate"],
                    profile_picture=user_data["profile_picture"],
                    role=user_data["permissions"],
                    created_at=created_at,
                    last_login=last_login,
                    wiki_roles=wiki_roles,
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
