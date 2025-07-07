from bottle import Bottle, redirect, request, response, template

from .base_controller import BaseController

home_routes = Bottle()


class HomeController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()
        self.base_controller = BaseController(app)

    def setup_routes(self):
        self.app.route("/", method="GET", callback=self.show_home)
        self.app.route("/home", method="GET", callback=self.show_home)
        self.app.route(
            "/home/create", method=["GET", "POST"], callback=self.create_wiki
        )

    def create_wiki(self):
        return self.render("home_form", action="/home/create")

    def show_home(self):
        from config import SECRET_KEY
        """Handle the home page request"""
        try:
            user = self.base_controller.get_current_user()
            print(f"DEBUG - User in controller: {user}")  # Add this line
            print(f"DEBUG - User ID: {user.id if user else 'None'}")
            recent_wikis = self.wiki_service.get_recent_wikis(limit=6)
        
            return self.render("home", 
                             recent_wikis=recent_wikis, 
                             error=None,
                             user=user)  # Make sure user is passed here
        except Exception as e:
            print(f"Error loading home: {str(e)}")
            return self.render(
                "home", 
                recent_wikis=[], 
                error="Could not load recent wikis",
                user=None
            )




home_controller = HomeController(home_routes)
