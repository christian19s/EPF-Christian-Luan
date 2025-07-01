from bottle import Bottle, redirect, request, response, template
from .base_controller import BaseController

home_routes = Bottle()

class HomeController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/home", method="GET", callback=self.home)
        self.app.route("/home/create", method=["GET","POST"], callback=self.create_wiki)

    def home(self):
        return self.render("home")

    def create_wiki(self):
        return self.render("home_form", action="/home/create")


home_controller = HomeController(home_routes)
