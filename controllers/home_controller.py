import os
import secrets

from .base_controller import BaseController
from services.home_service import HomeService

class HomeController(BaseController):
    def __init__(self, app):
        super().__init__(app)
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/home", method="GET", callback.self.list_hplinks)


    def list_hplinks(self):


