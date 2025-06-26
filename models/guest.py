from permSystem import PermissionSystem


class Guest:
    """Represents an unauthenticated visitor"""

    id = None
    username = "Guest"
    is_admin = False
    role = "guest"
    owned_wikis = None
    edited_pages = None

    def can(self, permission, wiki_id=None):
        """Check permissions for guest users"""
        # Guests can only view public content
        return permission in [
            PermissionSystem.VIEW_PAGE,
        ]

    def get_permission_labels(self, wiki_id=None):
        return ["View Public Content"]

    def get_wiki_role(self, wiki_id):
        return "guest"

    def is_authenticated(self):
        return False
