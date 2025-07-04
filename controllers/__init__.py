from bottle import Bottle

# from controllers.activity_controller import activity_routes NAO COMMITA SEUS TESTES!!!
from controllers.home_controller import home_routes
from controllers.user_controller import user_routes
from controllers.wiki_controller import wiki_routes


def init_controllers(app: Bottle):
    app.merge(user_routes)
    app.merge(home_routes)
    app.merge(wiki_routes)


#    app.merge(activity_routes)
