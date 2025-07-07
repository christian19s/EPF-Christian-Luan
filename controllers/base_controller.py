from bottle import response, request, static_file

from data import USER_UPLOADS


class BaseController:
    def __init__(self, app):
        self.app = app
        self._setup_base_routes()

    def _setup_base_routes(self):
        """Configura rotas básicas comuns a todos os controllers"""
        self.app.route("/", method="GET", callback=self.home_redirect)
        self.app.route("/helper", method=["GET"], callback=self.helper)
        # Rota para arquivos estáticos (CSS, JS, imagens)
        self.app.route("/static/<filename:path>", callback=self.serve_static)
        self.app.route(
            "/uploads/users/<filename:path>", callback=self.serve_user_uploads
        )

    # helper function:
    def render_error(self, message, status=500):
        """Render error page"""
        response.status = status
        return self.render_template(
            "error.tpl", error_message=message, status_code=status
        )

    def home_redirect(self):
        """Redireciona a rota raiz para /home"""
        return self.redirect("/home")

    def home(self):
        return self.render("home")

    def helper(self):
        return self.render("helper-final")

    def test(self):
        return self.render("testing")

    def serve_static(self, filename):
        """Serve arquivos estáticos da pasta static/"""
        return static_file(filename, root="./static")

    def render(self, template, **context):
        """Método auxiliar para renderizar templates"""
        from bottle import template as render_template

        return render_template(template, **context)

    def redirect(self, path):
        """Método auxiliar para redirecionamento"""
        from bottle import redirect as bottle_redirect

        return bottle_redirect(path)

    def serve_user_uploads(self, filename):
        return static_file(filename, root=str(USER_UPLOADS))

    def get_current_user(self):
        """Get authenticated user from session"""
        user_id = request.get_cookie("user_id", secret=SECRET_KEY)
        if user_id:
            return UserService.get_user_by_id(int(user_id))
        return None