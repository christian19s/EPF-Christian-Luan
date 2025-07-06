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
        self.role = role or PermissionSystem.DEFAULT_ROLES["global"]
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
    CREATE_WIKI = 128
    DELETE_WIKI = 256
    MANAGE_CATEGORIES = 512
    ROLES = {
        "viewer": VIEW_PAGE,
        "editor": VIEW_PAGE | EDIT_PAGE | CREATE_PAGE | MANAGE_CATEGORIES,
        "moderator": VIEW_PAGE
        | EDIT_PAGE
        | CREATE_PAGE
        | DELETE_PAGE
        | MANAGE_WIKI
        | MANAGE_CATEGORIES,
        "admin": (
            VIEW_PAGE
            | EDIT_PAGE
            | CREATE_PAGE
            | DELETE_PAGE
            | MANAGE_WIKI
            | MANAGE_USERS
            | CREATE_WIKI
            | ADMINISTER
            | MANAGE_CATEGORIES
        ),
        "superadmin": (
            VIEW_PAGE
            | EDIT_PAGE
            | CREATE_PAGE
            | DELETE_PAGE
            | MANAGE_WIKI
            | MANAGE_USERS
            | ADMINISTER
            | CREATE_WIKI
            | DELETE_WIKI
            | MANAGE_CATEGORIES
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
        CREATE_WIKI: "Create new wikis",
    }

    @staticmethod
    def has_permission(user_permissions, required_permission):
        """Check if permissions include the required permission"""
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
        # superadmin tem a admin em todas
        if PermissionSystem.has_permission(
            user.permissions, PermissionSystem.ADMINISTER
        ):
            return "superadmin"
        # dono de uma wiki e admin
        if wiki_id and hasattr(user, "owned_wikis"):
            if any(wiki.id == wiki_id for wiki in user.owned_wikis):
                return "admin"

        if wiki_id and hasattr(user, "wiki_roles"):
            if wiki_id in user.wiki_roles:
                return user.wiki_roles[wiki_id]
        # se usuario
        return getattr(user, "role", "viewer")

    @staticmethod
    def can(user, permission, wiki_id=None):
        """Check user permission in the context of a wiki"""
        if user is None:
            return False
        role = PermissionSystem.get_role_for_context(user, wiki_id)
        print(f"Required permission: {permission}")
        print(f"user has: {user.global_role} as global")
        print(f"user has: {user.wiki_roles}")

        # checa as permissoes para essa role
        role_permissions = PermissionSystem.get_role_permissions(role)

        return PermissionSystem.has_permission(role_permissions, permission)

    @staticmethod
    def get_role_for_context(user, wiki_id=None):
        """Determine user's role in a specific context"""
        # superadm e super adm em todas as wikis
        if user.global_role == "superadmin":
            return "superadmin"
        # usuario e admin em todas as wikis que ele criou
        if wiki_id and wiki_id in user.owned_wikis:
            return "admin"

        if wiki_id and str(wiki_id) in user.wiki_roles:
            return user.wiki_roles[str(wiki_id)]

        # 4. Fallback to global role
        return user.global_role

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
