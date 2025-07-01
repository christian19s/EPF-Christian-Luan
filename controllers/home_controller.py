from bottle import Bottle, redirect, request, response, template
from .base_controller import BaseController

home_routes = Bottle()

class HomeController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/home", method="GET", callback=self.home)
        self.app.route("/home/add", method=["GET","POST"], callback=self.add_wiki)

    def home(self):
        return self.render("home")

    def add_wiki(self):
        return self.render("home_add", action="/home/add")


home_controller = HomeController(home_routes)
