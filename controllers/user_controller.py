import os
import secrets

from bottle import Bottle, redirect, request, response, template
from models.auth_user import UPLOAD_DIR, AuthUser
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
        self.app.route("/login")

    #   def login():
    #    return self.service.login()

    def list_users(self):
        users = self.user_service.get_all()
        return self.render("users", users=users)

    def add_user(self):
        if request.method == "GET":
            return self.render("user_form", user=None, action="/users/add")
        else:
            # Extract form data
            username = request.forms.get("username")
            email = request.forms.get("email")
            password = request.forms.get("password")
            birthdate = request.forms.get("birthdate")

            # Handle profile picture
            profile_picture = self._handle_profile_picture_upload()

            # Create new user
            self.user_service.create_user(
                username=username,
                email=email,
                password=password,
                birthdate=birthdate,
                profile_picture=profile_picture,
            )
            self.redirect("/users")

    def edit_user(self, user_id):
        user = self.user_service.get_by_id(user_id)
        if not user:
            return "Usuário não encontrado"

        if request.method == "GET":
            return self.render("user_form", user=user, action=f"/users/edit/{user_id}")
        else:
            # Extract form data
            username = request.forms.get("username")
            email = request.forms.get("email")
            password = request.forms.get("password")
            birthdate = request.forms.get("birthdate")

            # Handle profile picture
            profile_picture = self._handle_profile_picture_upload(user.profile_picture)

            # Update user
            self.user_service.update_user(
                user_id=user_id,
                username=username,
                email=email,
                password=password,  # Will be hashed if provided
                birthdate=birthdate,
                profile_picture=profile_picture,
            )
            self.redirect("/users")

    def delete_user(self, user_id):
        self.user_service.delete_user(user_id)
        self.redirect("/users")


@user_routes.route("/login", method=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.forms.get("username")
        password = request.forms.get("password")

        # Authenticate user
        user = AuthUser.authenticate(username, password)

        if user:
            # Set session cookie
            response.set_cookie(
                "user_id", str(user.id), path="/", secret=YOUR_SECRET_KEY
            )

            # Update last login
            with closing(get_db_connection()) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
                    (user.id,),
                )
                conn.commit()

            redirect("/dashboard")
        else:
            error = "Credenciais inválidas. Por favor tente novamente."

    return template("login", error=error)


@user_routes.route("/register", method=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.forms.get("username")
        email = request.forms.get("email")
        password = request.forms.get("password")
        confirm_password = request.forms.get("confirm_password")

        # Basic validation
        if not all([username, email, password, confirm_password]):
            error = "Todos os campos são obrigatórios."
        elif password != confirm_password:
            error = "As senhas não coincidem."
        else:
            # Check if username/email exists
            if user_service.username_exists(username):
                error = "Nome de usuário já está em uso."
            elif user_service.email_exists(email):
                error = "Email já está em uso."
            else:
                # Create new user
                password_hash = generate_password_hash(password)
                user_id = user_service.create_user(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    role="user",  # Default role
                )

                if user_id:
                    # Auto-login after registration
                    response.set_cookie(
                        "user_id", str(user_id), path="/", secret=SECRET_KEY
                    )
                    redirect("/dashboard")
                else:
                    error = "Erro ao criar conta. Por favor tente novamente."

    return template("register", error=error)


user_controller = UserController(user_routes)
