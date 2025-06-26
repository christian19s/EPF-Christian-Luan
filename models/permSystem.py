from ast import Constant


class PermissionSystem:
    # Perm Const
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
        "admin": VIEW_PAGE
        | EDIT_PAGE
        | CREATE_PAGE
        | DELETE_PAGE
        | MANAGE_WIKI
        | MANAGE_USERS,
        "superadmin": VIEW_PAGE
        | EDIT_PAGE
        | CREATE_PAGE
        | DELETE_PAGE
        | MANAGE_WIKI
        | MANAGE_USERS
        | ADMINISTER,
    }

    # default role assignments
    DEFAULT_ROLES = {
        "global": "viewer",
        "owned_wikis": "admin",  # user owns wiki
    }

    # Permission mappings for ui:
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
        return (user_permissions & required_permission) == required_permission

    @staticmethod
    def get_role_permissions(role_name):
        """Get permission bitmask for a role"""
        return PermissionSystem.ROLES.get(role_name, PermissionSystem.ROLES["viewer"])

    @staticmethod
    def get_permission_labels(permission_mask):
        """Get human-readable permission names from bitmask"""
        return [
            label
            for perm, label in PermissionSystem.PERMISSION_LABELS.items()
            if (permission_mask & perm) == perm
        ]

    @staticmethod
    def get_role_for_context(user, wiki_id=None):
        # Superadmin has all permissions everywhere
        if PermissionSystem.has_permission(
            user.permissions, PermissionSystem.ADMINISTER
        ):
            return "superadmin"

        # Check if user owns the wiki
        if wiki_id and wiki_id in [w.id for w in user.owned_wikis]:
            return "admin"

        # Check wiki-specific role
        if wiki_id and wiki_id in user.wiki_roles:
            return user.wiki_roles[wiki_id]

        # Fallback to global role
        return user.role

    @staticmethod
    def can(user, permission, wiki_id=None):
        """Check user permission in the context of a wiki"""
        role = PermissionSystem.get_role_for_context(user, wiki_id)
        role_permissions = PermissionSystem.get_role_permissions(role)
        return PermissionSystem.has_permission(role_permissions, permission)

    @staticmethod
    def get_all_roles():
        """Get all defined roles"""
        return list(PermissionSystem.ROLES.keys())
