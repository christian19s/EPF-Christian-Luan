from bottle import Bottle

from config import Config
from controllers.admin_controller import admin
from data import init_db


class App:
    def __init__(self):
        self.bottle = Bottle()
        self.config = Config()
        init_db()

    def setup_routes(self):
        from controllers import init_controllers

        print("🚀 Inicializa rotas!")
        init_controllers(self.bottle)

    def run(self):
        admin.create_admin_user()
        self.setup_routes()
        self.bottle.run(
            host=self.config.HOST,
            port=self.config.PORT,
            debug=self.config.DEBUG,
            reloader=self.config.RELOADER,
        )


def create_app():
    return App()
