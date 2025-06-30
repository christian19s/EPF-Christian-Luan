import datetime
import hashlib
import json
import os
from contextlib import closing

# In models/user.py
import bcrypt
from config import BASE_DIR, UPLOAD_DIR
from data import get_db_connection

from .permSystem import PermissionSystem


def generate_password_hash(password):
    """Generate secure password hash using bcrypt"""
    salt = bcrypt.gensalt()
    password_bytes = str(password).encode("utf-8")
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(password, password_hash):
    print(f"Verifying password against hash: {password_hash}")
    try:
        password_bytes = password.encode("utf-8")
        password_hash_bytes = password_hash.encode("utf-8")
        result = bcrypt.checkpw(password_bytes, password_hash_bytes)
        print(f"Password match: {result}")
        return result
    except Exception as e:
        print(f"Password verification error: {str(e)}")
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
        self.permissions = role or PermissionSystem.DEFAULT_ROLES["global"]
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

    def create_user(username, email, password, birthdate=None, profile_picture=None):
        """Create and save a new user to the database"""
        password_hash = generate_password_hash(password)
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        wiki_roles_json = json.dumps({})  # roles são inicializadas vazias
        role = PermissionSystem.DEFAULT_ROLES["global"]  # permisssa default
        with closing(get_db_connection()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (
                    username, 
                    email, 
                    permissions,
                    password_hash, 
                    birthdate, 
                    profile_picture,  
                    created_at, 
                    wiki_roles
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    email,
                    role,  # role = permission nesse caso.
                    password_hash,
                    birthdate,
                    profile_picture,
                    created_at,
                    wiki_roles_json,
                ),
            )
            user_id = cursor.lastrowid
            conn.commit()

        return AuthUser(
            id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            birthdate=birthdate,
            profile_picture=profile_picture,
            role=role,
            created_at=created_at,
            wiki_roles={},
        )


def update_last_login(self):
    """Update last login timestamp"""
    new_last_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (new_last_login, self.id),
        )
        conn.commit()
    self.last_login = new_last_login
