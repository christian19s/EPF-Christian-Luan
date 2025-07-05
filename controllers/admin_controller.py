from services.user_service import UserService

from .user_controller import UserController


class admin(UserController):
    @staticmethod
    def create_admin_user():
        """Create admin user if none exists"""

    try:
        if not UserService.get_user_by_username("admin"):
            UserService.create_user(
                username="admin",
                email="admin@example.com",
                password="adminpassword",
                global_role="admin",
            )
            print("Created admin user")
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
