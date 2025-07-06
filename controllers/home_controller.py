from bottle import Bottle, redirect, request, response, template
from .base_controller import BaseController

home_routes = Bottle()

class HomeController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/", method="GET", callback=self.show_home)
        self.app.route("/home", method="GET", callback=self.show_home)
        self.app.route("/home/create", method=["GET","POST"], callback=self.create_wiki)

    def create_wiki(self):
        return self.render("home_form", action="/home/create")

    def show_home(self):
        """Handle the home page request"""
        try:
            # Get recent wikis from your database/service
            recent_wikis = self.wiki_service.get_recent_wikis(limit=6)
        
            return self.render("home", 
                            recent_wikis=recent_wikis,
                            error=None)
        except Exception as e:
            print(f"Error loading home: {str(e)}")
            return self.render("home",
                            recent_wikis=[],
                            error="Could not load recent wikis")


home_controller = HomeController(home_routes)
