import json
import os
from contextlib import closing

import bcrypt  # Corrected import name
from db import get_db_connection

from .permSystem import PermissionSystem

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "profiles")


def generate_password_hash(password):
    """Generate secure password hash using bcrypt"""
    # Generate salt and hash with bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password, password_hash):
    """Verify password against stored bcrypt hash"""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


class AuthUser:
    """Base class for all authenticated users"""

    def __init__(
        self,
        id,
        username,
        email,
        password_hash,
        birthdate=None,
        profile_picture=None,
        role=None,
        permissions=0,
        created_at=None,
        last_login=None,
        wiki_roles=None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.birthdate = birthdate
        self.profile_picture = profile_picture
        self.role = role or PermissionSystem.DEFAULT_ROLES["global"]
        self.permissions = permissions
        self.created_at = created_at
        self.last_login = last_login
        self.wiki_roles = wiki_roles or {}
        self.owned_wikis = []
        self.edited_pages = []

    def is_authenticated(self):
        return True

    def is_admin(self):
        return False

    def get_permissions(self, wiki_id=None):
        return PermissionSystem.get_role_permissions(
            PermissionSystem.get_role_for_context(self, wiki_id)
        )

    def can(self, permission, wiki_id=None):
        return PermissionSystem.can(self, permission, wiki_id)

    def get_permission_labels(self, wiki_id=None):
        return PermissionSystem.get_permission_labels(self.get_permissions(wiki_id))

    def get_wiki_role(self, wiki_id):
        return PermissionSystem.get_role_for_context(self, wiki_id)

    def set_wiki_role(self, wiki_id, role_name):
        if role_name not in PermissionSystem.ROLES:
            raise ValueError(f"Invalid role: {role_name}")
        self.wiki_roles[wiki_id] = role_name

        # Update database
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET wiki_roles = ? WHERE id = ?",
                (json.dumps(self.wiki_roles), self.id),
            )
            conn.commit()

    def get_profile_picture_url(self):
        """Get URL for profile picture with OS-agnostic path handling"""
        if self.profile_picture:
            # Use forward slashes for URLs regardless of OS
            return os.path.join(
                "/", "uploads", "profiles", self.profile_picture
            ).replace("\\", "/")
        return os.path.join("/", "static", "images", "default-profile.png").replace(
            "\\", "/"
        )

    def update_profile(self, **kwargs):
        allowed_fields = ["username", "email", "birthdate", "profile_picture"]
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not updates:
            return False

        set_clause = ", ".join([f"{field} = ?" for field in updates.keys()])
        values = list(updates.values())
        values.append(self.id)

        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
            conn.commit()

            # Update instance properties
            for field, value in updates.items():
                setattr(self, field, value)

            return True

    def change_password(self, new_password):
        """Securely change password using bcrypt"""
        password_hash = generate_password_hash(new_password)
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (password_hash, self.id),
            )
            conn.commit()
            self.password_hash = password_hash
            return True

    def verify_password(self, password):
        """Verify provided password against stored hash using bcrypt"""
        return verify_password(password, self.password_hash)
