import os
import secrets
import sqlite3
import traceback
from contextlib import closing

from bottle import Bottle, HTTPError, HTTPResponse, redirect, request, response

from config import SECRET_KEY
from data import BASE_DIR, get_db_connection
from models.user import AuthUser
from services.exceptions import (AuthenticationFailed, DuplicateUser,
                                 UserNotFound)
from services.user_service import UserService

from .base_controller import BaseController

user_routes = Bottle()


class UserController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()
        self.user_service = UserService()

    def get_current_user_id(self):
        print("trying to get an id:")
        return request.get_cookie("user_id", secret=SECRET_KEY)

    # Rotas User
    def setup_routes(self):
        self.app.route("/login", method=["GET", "POST"], callback=self.login)
        self.app.route("/register", method=["GET", "POST"], callback=self.register)
        self.app.route("/dashboard", method="GET", callback=self.dashboard)
        self.app.route(
            "/dashboard/update_profile_picture",
            method="POST",
            callback=self.update_profile_picture,
        )
        self.app.route("/change-password", method=["GET","POST"], callback=self.change_password)
        self.app.route("/logout", method=["GET","POST"], callback=self.logout)

    def list_users(self):
        try:
            users = self.user_service.get_all_users()
            return self.render("users", users=users)
        except Exception as e:
            return self.render_error(f"Error loading users: {str(e)}")

    def add_user(self):
        if request.method == "GET":
            return self.render("user_form", user=None, action="/users/add", errors=None)

        username = request.forms.get("username", "").strip()
        email = request.forms.get("email", "").strip()
        password = request.forms.get("password", "").strip()
        birthdate = request.forms.get("birthdate", "").strip()
        profile_picture = self._handle_profile_picture_upload()

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

        username = request.forms.get("username", "").strip()
        email = request.forms.get("email", "").strip()
        birthdate = request.forms.get("birthdate", "").strip()
        profile_picture = self._handle_profile_picture_upload(user.profile_picture)

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
            return self.render(f"Error deleting user: {str(e)}")

    def dashboard(self):
        print("attempting to load dashboard")
        user_id = self.get_current_user_id()
        print(f"Retrieved user_id from cookie: {user_id}")

        if not user_id:
            print("No user ID found, redirecting to login")
            return redirect("/login")

        try:
            print(f"Fetching user with ID: {user_id}")
            user = self.user_service.get_user_by_id(user_id)

            if not user:
                print(f"No user found for ID {user_id}")
                return redirect("/login")

            print(f"User found: {user.username} (ID: {user.id})")
            print("Fetching edited pages...")
            edited_pages = []
            print(f"Found {len(edited_pages)} edited pages")

            return self.render("dashboard", user=user, edited_pages=edited_pages)
        except Exception as e:
            print(f"Error loading dashboard: {str(e)}")
            import traceback

            traceback.print_exc()
            return self.render(f"Error loading dashboard: {str(e)}")

    def login(self):
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
                    print(f"logged in as {str(user.id)}")
                    response.set_cookie(
                        "user_id", str(user.id), path="/", secret=SECRET_KEY
                    )
                    print(f"Response headers: {response.headers}")
                    print("logged in baby!, will be redirected to dashboard")
                    return redirect("/dashboard")
            except (AuthenticationFailed, UserNotFound) as e:
                error = "Credencial invalida"
            except HTTPError as e:
                raise
        return self.render("login", error=error)

    def logout(self):
        """Handle user logout by clearing session cookies and redirecting"""
       # Clear the user_id cookie
        response.delete_cookie("user_id", path="/")
    
        # Optionally clear any other auth-related cookies
        response.delete_cookie("session_token", path="/")  # if you use additional session tokens
    
        # Add a flash message (if your system supports it)
        try:
            flash("You have been logged out successfully")  # Requires flash messaging setup
        except:
            pass
    
        # Redirect to login page with a 303 See Other status to prevent form resubmission
        response.status = 303
        response.headers["Location"] = "/login"
        return response

    def change_password(self):
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect("/login")

        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return redirect("/login")

        if request.method == "POST":
            current_password = request.forms.get("current_password", "").strip()
            new_password = request.forms.get("new_password", "").strip()
            confirm_password = request.forms.get("confirm_password", "").strip()

            try:
                user = self.user_service.change_password(
                    user_id=user_id,
                    current_password=current_password,
                    new_password=new_password
                )
                return self.render("change_password", 
                           success="Password changed successfully",
                           error=None,
                           user_password=new_password)  # Show the new password
            except AuthenticationFailed:
                return self.render("change_password",
                           error="Current password is incorrect",
                           success=None,
                           user_password=current_password)  # Keep showing what they typed
            except Exception as e:
                return self.render("change_password",
                           error=f"Error: {str(e)}",
                           success=None,
                           user_password=current_password)

        # For GET requests, show the current password (SECURITY RISK!)
        return self.render("change_password", 
                       error=None, 
                       success=None,
                       user_password=user.password_hash)  # Or use a decrypted version if available

    def register(self):
        """Handle user registration"""
        error = None
        print("attempting to create user")

        if request.method == "POST":
            username = request.forms.get("username", "").strip()
            email = request.forms.get("email", "").strip()
            password = request.forms.get("password", "").strip()
            confirm_password = request.forms.get("confirm_password", "").strip()

            # Validation
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
                print(f"attempting to create user {username}")
                user = AuthUser.create_user(
                    username=username, email=email, password=password
                )

                # Set cookie
                response.set_cookie(
                    "user_id", str(user.id), path="/", secret=SECRET_KEY
                )
                print(f"Cookie set for user: {user.id}")

                response.status = 303
                response.headers["Location"] = "/dashboard"
                return response

            except DuplicateUser as e:
                error = str(e)
            except Exception as e:
                error = f"Error creating account: {str(e)}"
                print(f"Registration error: {traceback.format_exc()}")

        return self.render("register", error=error)

    def update_profile_picture(self):
        user_id = self.get_current_user_id()
        if not user_id:
            return HTTPResponse(status=401, body="Unauthorized")

        try:
            user = self.user_service.get_user_by_id(user_id)
            if not user:
                return HTTPResponse(status=404, body="User not found")

            old_filename = user.profile_picture
            new_filename = self._handle_profile_picture_upload(old_filename)

            if new_filename and new_filename != old_filename:
                self.user_service.update_user_profile(
                    user_id=user_id, profile_picture=new_filename
                )
                # Return new image HTML
                new_url = f"/uploads/users/{new_filename}"
                return f'<img src="{new_url}" alt="Profile Picture" class="profile-picture" id="profileImage">'
            else:
                # Return current image if no change
                return f'<img src="{user.get_profile_picture_url()}" alt="Profile Picture" class="profile-picture" id="profileImage">'
        except Exception as e:
            print(f"Error: {str(e)}")
            traceback.print_exc()
            return HTTPResponse(status=500, body="Error updating profile")

    def _handle_profile_picture_upload(self, old_filename=None):
        from data import get_user_upload_path

        UPLOAD_DIR = get_user_upload_path()

        profile_picture = request.files.get("profile_picture")
        if not profile_picture or not profile_picture.filename:
            return old_filename

        # Extract file extension
        ext = os.path.splitext(profile_picture.filename)[1].lower().strip()
        if not ext:
            return old_filename

        # Generate new filename
        filename = secrets.token_hex(8) + ext

        # Validate file size
        MAX_SIZE = 20 * 1024 * 1024  # 20MB
        file_size = len(profile_picture.file.read())
        profile_picture.file.seek(0)

        if file_size > MAX_SIZE:
            return old_filename

        # Validate file type
        if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            return old_filename

        try:
            # Ensure directory exists
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

            # Save file
            new_file_path = UPLOAD_DIR / filename
            profile_picture.save(str(new_file_path), overwrite=True)

            # Delete old file
            if old_filename:
                old_file_path = UPLOAD_DIR / old_filename
                if old_file_path.exists():
                    old_file_path.unlink()

            return filename
        except Exception as e:
            print(f"Upload error: {str(e)}")
            traceback.print_exc()
            return old_filename  # ===========================ADMIN USER==================================+#


user_controller = UserController(user_routes)
