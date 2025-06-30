import os
import secrets
from contextlib import closing

from bottle import Bottle, redirect, request, response, template
from config import SECRET_KEY, UPLOAD_DIR
from data import get_db_connection
from models.user import AuthUser
from services.exceptions import AuthenticationFailed, DuplicateUser, UserNotFound
from services.user_service import UserService

from .base_controller import BaseController

user_routes = Bottle()


class UserController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()
        self.user_service = UserService()

    # Helper for profile picture uploads
    def _handle_profile_picture_upload(self, old_filename=None):
        """Handle profile picture upload and return new filename"""
        profile_picture = request.files.get("profile_picture")
        if not profile_picture or not profile_picture.filename:
            return old_filename  # No new file uploaded

        # Generate secure filename
        ext = os.path.splitext(profile_picture.filename)[1]
        filename = secrets.token_hex(8) + ext

        # Ensure upload directory exists
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        # Save new file
        file_path = os.path.join(UPLOAD_DIR, filename)
        profile_picture.save(file_path)

        # Delete old file if it exists
        if old_filename and old_filename != filename:
            old_path = os.path.join(UPLOAD_DIR, old_filename)
            if os.path.exists(old_path):
                os.remove(old_path)

        return filename

    # Rotas User
    def setup_routes(self):
        self.app.route("/users", method="GET", callback=self.list_users)
        self.app.route("/users/add", method=["GET", "POST"], callback=self.add_user)
        self.app.route(
            "/users/edit/<user_id:int>", method=["GET", "POST"], callback=self.edit_user
        )
        self.app.route(
            "/users/delete/<user_id:int>", method="POST", callback=self.delete_user
        )
        self.app.route("/login", method=["GET", "POST"], callback=self.login)
        self.app.route("/register", method=["GET", "POST"], callback=self.register)

    def list_users(self):
        try:
            users = self.user_service.get_all_users()
            return self.render("users", users=users)
        except Exception as e:
            return self.render_error(f"Error loading users: {str(e)}")

    def add_user(self):
        if request.method == "GET":
            return self.render("user_form", user=None, action="/users/add", errors=None)

        # Extract form data
        username = request.forms.get("username", "").strip()
        email = request.forms.get("email", "").strip()
        password = request.forms.get("password", "").strip()
        birthdate = request.forms.get("birthdate", "").strip()
        profile_picture = self._handle_profile_picture_upload()

        # Validate inputs
        errors = []
        if not username:
            errors.append("Username is required")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")

        if errors:
            return self.render(
                "user_form", user=None, action="/users/add", errors=errors
            )

        try:
            # Create new user
            self.user_service.create_user(
                username=username,
                email=email,
                password=password,
                birthdate=birthdate or None,
                profile_picture=profile_picture,
            )
            return redirect("/users")
        except DuplicateUser as e:
            errors = [str(e)]
            return self.render(
                "user_form", user=None, action="/users/add", errors=errors
            )
        except Exception as e:
            errors = [f"Error creating user: {str(e)}"]
            return self.render(
                "user_form", user=None, action="/users/add", errors=errors
            )

    def edit_user(self, user_id):
        try:
            user = self.user_service.get_user_by_id(user_id)
            if not user:
                return self.render_error("User not found")
        except UserNotFound:
            return self.render_error("User not found")

        if request.method == "GET":
            return self.render(
                "user_form", user=user, action=f"/users/edit/{user_id}", errors=None
            )

        # Extract form data
        username = request.forms.get("username", "").strip()
        email = request.forms.get("email", "").strip()
        birthdate = request.forms.get("birthdate", "").strip()
        profile_picture = self._handle_profile_picture_upload(user.profile_picture)

        # Validate inputs
        errors = []
        if not username:
            errors.append("Username is required")
        if not email:
            errors.append("Email is required")

        if errors:
            return self.render(
                "user_form", user=user, action=f"/users/edit/{user_id}", errors=errors
            )

        try:
            # Update user profile
            self.user_service.update_user_profile(
                user_id=user_id,
                username=username,
                email=email,
                birthdate=birthdate or None,
                profile_picture=profile_picture,
            )
            return redirect("/users")
        except Exception as e:
            errors = [f"Error updating user: {str(e)}"]
            return self.render(
                "user_form", user=user, action=f"/users/edit/{user_id}", errors=errors
            )

    def delete_user(self, user_id):
        try:
            self.user_service.delete_user(user_id)
            return redirect("/users")
        except Exception as e:
            return self.render_error(f"Error deleting user: {str(e)}")

    def login(self):
        """Handle user login"""
        error = None
        if request.method == "POST":
            print("Form data:", request.forms)
            username = request.forms.get("username", "").strip()
            password = request.forms.get("password", "").strip()
            print(f"Username: '{username}', Password: '{password}'")
            try:
                # Authenticate user
                print("trying to auth user")
                print(f"Login attempt for: {username}")
                print(f"Login attempt - Username: {username}, Password: {password}")
                user = self.user_service.authenticate_user(username, password)
                print(f"Authentication result: {user.id if user else 'None'}")
                if user:
                    # Set session cookie
                    response.set_cookie(
                        "user_id", str(user.id), path="/", secret=SECRET_KEY
                    )

                    # Update last login
                    # user.update_last_login()

                    print("logged in baby!")
                    # return redirect("/dashboard")

                else:
                    error = "Invalid credentials. Please try again."
            except AuthenticationFailed as e:
                error = str(e)
            except Exception as e:
                error = f"Login error: {str(e)}"
                print("something went wrong")
        return self.render("login", error=error)

    def register(self):
        """Handle user registration"""
        error = None
        if request.method == "POST":
            username = request.forms.get("username", "").strip()
            email = request.forms.get("email", "").strip()
            password = request.forms.get("password", "").strip()
            confirm_password = request.forms.get("confirm_password", "").strip()

            # Basic validation
            errors = []
            if not username:
                errors.append("Username is required")
            if not email:
                errors.append("Email is required")
            if not password:
                errors.append("Password is required")
            if password != confirm_password:
                errors.append("Passwords do not match")

            if errors:
                return self.render("register", errors=errors)

            try:
                # Create new user
                user = self.user_service.create_user(
                    username=username, email=email, password=password
                )

                # Auto-login after registration
                response.set_cookie(
                    "user_id", str(user.id), path="/", secret=SECRET_KEY
                )
                return redirect("/dashboard")
            except DuplicateUser as e:
                error = str(e)
            except Exception as e:
                error = f"Error creating account: {str(e)}"

        return self.render("register", error=error)


user_controller = UserController(user_routes)
