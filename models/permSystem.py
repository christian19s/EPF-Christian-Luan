class AuthUser:
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
        self.role = (
            role or PermissionSystem.DEFAULT_ROLES["global"]
        )  # Add role attribute
        self.permissions = permissions
        self.created_at = created_at
        self.last_login = last_login
        self.wiki_roles = wiki_roles or {}
        self.owned_wikis = []
        self.edited_pages = []

    def can(self, permission, wiki_id=None):
        """Check if user has a specific permission"""
        return PermissionSystem.can(self, permission, wiki_id)


class PermissionSystem:
    # Permission constants
    VIEW_PAGE = 1
    EDIT_PAGE = 2
    CREATE_PAGE = 4
    DELETE_PAGE = 8
    MANAGE_WIKI = 16
    MANAGE_USERS = 32
    ADMINISTER = 64

    ROLES = {
        "viewer": VIEW_PAGE,
        "editor": VIEW_PAGE | EDIT_PAGE | CREATE_PAGE,
        "moderator": VIEW_PAGE | EDIT_PAGE | CREATE_PAGE | DELETE_PAGE | MANAGE_WIKI,
        "admin": (
            VIEW_PAGE
            | EDIT_PAGE
            | CREATE_PAGE
            | DELETE_PAGE
            | MANAGE_WIKI
            | MANAGE_USERS
        ),
        "superadmin": (
            VIEW_PAGE
            | EDIT_PAGE
            | CREATE_PAGE
            | DELETE_PAGE
            | MANAGE_WIKI
            | MANAGE_USERS
            | ADMINISTER
        ),
    }

    DEFAULT_ROLES = {
        "global": "viewer",
        "owned_wikis": "admin",
    }

    PERMISSION_LABELS = {
        VIEW_PAGE: "View Pages",
        EDIT_PAGE: "Edit Pages",
        CREATE_PAGE: "Create Pages",
        DELETE_PAGE: "Delete Pages",
        MANAGE_WIKI: "Manage Wiki Settings",
        MANAGE_USERS: "Manage Users",
        ADMINISTER: "System Administration",
    }

    @staticmethod
    def has_permission(user_permissions, required_permission):
        """Check if permissions include the required permission"""
        # Convert to int if needed
        if isinstance(user_permissions, str):
            try:
                user_permissions = int(user_permissions)
            except ValueError:
                return False
        return (user_permissions & required_permission) == required_permission

    @staticmethod
    def get_role_permissions(role_name):
        """Get permission bitmask for a role"""
        return PermissionSystem.ROLES.get(role_name, 0)

    @staticmethod
    def get_permission_labels(permission_mask):
        """Get human-readable permission names from bitmask"""
        # Convert to int if needed
        if isinstance(permission_mask, str):
            try:
                permission_mask = int(permission_mask)
            except ValueError:
                return []

        return [
            label
            for perm, label in PermissionSystem.PERMISSION_LABELS.items()
            if permission_mask & perm
        ]

    @staticmethod
    def get_role_for_context(user, wiki_id=None):
        """Determine user's role in a specific context"""
        # Superadmin has all permissions everywhere
        if PermissionSystem.has_permission(
            user.permissions, PermissionSystem.ADMINISTER
        ):
            return "superadmin"

        # Check if user owns the wiki
        if wiki_id and hasattr(user, "owned_wikis"):
            if any(wiki.id == wiki_id for wiki in user.owned_wikis):
                return "admin"

        # Check wiki-specific role
        if wiki_id and hasattr(user, "wiki_roles"):
            if wiki_id in user.wiki_roles:
                return user.wiki_roles[wiki_id]

        # Fallback to global role
        return getattr(user, "role", "viewer")

    @staticmethod
    def can(user, permission, wiki_id=None):
        """Check user permission in the context of a wiki"""
        # Handle unauthenticated users
        if user is None or not hasattr(user, "permissions"):
            return False

        role = PermissionSystem.get_role_for_context(user, wiki_id)
        role_permissions = PermissionSystem.get_role_permissions(role)
        return PermissionSystem.has_permission(role_permissions, permission)

    @staticmethod
    def get_all_roles():
        """Get all defined roles"""
        return list(PermissionSystem.ROLES.keys())

    @staticmethod
    def get_permission_name(permission_value):
        """Get human-readable name for a permission value"""
        return PermissionSystem.PERMISSION_LABELS.get(
            permission_value, "Unknown Permission"
        )
