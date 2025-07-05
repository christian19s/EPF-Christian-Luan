import os
import secrets
import sqlite3
import traceback
from contextlib import closing

from bottle import Bottle, HTTPError, redirect, request, response
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
        self.app.route("/dashboard/update_profile_picture",method="POST",
            callback=self.update_profile_picture,
        )
 




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
            edited_pages = self.get_edited_pages(user_id)
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

    def register(self):
        """Handle user registration"""
        error = None
        if request.method == "POST":
            username = request.forms.get("username", "").strip()
            email = request.forms.get("email", "").strip()
            password = request.forms.get("password", "").strip()
            confirm_password = request.forms.get("confirm_password", "").strip()
            # validando input
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
                # Cria novo usuario, outros atributos são tratados em dashboard:
                user = self.user_service.create_user(
                    username=username, email=email, password=password
                )
                response.set_cookie(
                    "user_id", str(user.id), path="/", secret=SECRET_KEY
                )
                return redirect("/dashboard")
            except DuplicateUser as e:
                error = str(e)
            except Exception as e:
                error = f"Error creating account: {str(e)}"
        return self.render("register", error=error)

    def update_profile_picture(self):
        user_id = self.get_current_user_id()
        if not user_id:
            return redirect("/login")
        redirect_url = request.headers.get("Referer", "/profile")
        try:
            user = self.user_service.get_user_by_id(user_id)
            if not user:
                return redirect("/login")
            old_filename = user.profile_picture
            new_filename = self._handle_profile_picture_upload(old_filename)

            self.user_service.update_user_profile(
                user_id=user_id, profile_picture=new_filename
            )
        except Exception as e:
            if e != "":
                print(f"error: {e}")
            else:
                print("this was caught here")
    
        return redirect(redirect_url)

    def get_edited_pages(self, user_id):
        """Retrieve pages edited by the user"""
        user_id = UserService.get_user_by_id(user_id)
        print("attempting to get data")
        try:
            with closing(get_db_connection()) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                SELECT 
                    pages.id AS page_id,
                    pages.title AS page_title,
                    wikis.id AS wiki_id,
                    wikis.name AS wiki_name,
                    page_edit_history.edit_time
                FROM page_edit_history
                JOIN pages ON page_edit_history.page_id = pages.id
                JOIN wikis ON pages.wiki_id = wikis.id
                WHERE page_edit_history.user_id = ?
                ORDER BY page_edit_history.edit_time DESC
                LIMIT 50
            """,
                    (user_id,),
                )
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            print(f"Error fetching edited pages: {str(e)}")
        return []

    def _handle_profile_picture_upload(self, old_filename=None):
        from data import get_user_upload_path

        UPLOAD_DIR = get_user_upload_path()
        print("trying to upload profile picture")
        profile_picture = request.files.get("profile_picture")
        if not profile_picture or not profile_picture.filename:
            return old_filename
        print(f"file recieved {old_filename}")
        print(f"UPLOAD_DIR: {UPLOAD_DIR}")
        print(f"Current working directory: {os.getcwd()}")
        ext = os.path.splitext(profile_picture.filename)[1].lower()
        ext = ext.strip().lower()
        filename = secrets.token_hex(8) + ext

        MAX_SIZE = 20 * 1024 * 1024
        profile_picture.file.seek(0, 2)
        file_size = profile_picture.file.tell()
        profile_picture.file.seek(0)

        if file_size > MAX_SIZE:
            print(f"file {file_size} too large, aborting ")
            return old_filename

        if ext not in (".jpg", ".jpeg", ".png", ".gif"):
            print("invalid format detected")
            return old_filename
        absolute_path = UPLOAD_DIR/ filename
        try:

            os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
            print(f"Saving to: {absolute_path}")

            with open(absolute_path, "wb") as f:
                chunk_size = 20000
                while True:
                    chunk = profile_picture.file.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)

            print(f"Successfully saved to {absolute_path}")


            # Delete old file if it exists
            if old_filename:
                old_abs_path = UPLOAD_DIR/ "uploads" / old_filename
                print(f"olf file found at: {old_abs_path}")
                if os.path.exists(old_abs_path):
                    try:
                        os.remove(old_abs_path)
                        print(f"Deleted old file: {old_abs_path}")
                    except Exception as e:
                        print(f"Could not delete old file: {str(e)}")

            return filename

        except Exception as e:
            print(f"Upload error: {str(e)}")
            traceback.print_exc()
            return old_filename


user_controller = UserController(user_routes)
