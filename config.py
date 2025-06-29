import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "images")


class Config:
    # Configurações do servidor
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 8080))
    DEBUG = os.environ.get("DEBUG", "True") == "True"
    RELOADER = os.environ.get("RELOADER", "True") == "True"

    # Paths
    TEMPLATE_PATH = os.path.join(BASE_DIR, "views")
    STATIC_PATH = os.path.join(BASE_DIR, "static")
    DATA_PATH = os.path.join(BASE_DIR, "data")
    DB_PATH = os.path.join(BASE_DIR, DATA_PATH, "db")
    # Outras configurações
    SECRET_KEY = "9fd7c7658bc3640c974f93e9b69f1d17eb1bf812ab53ca9350250c6b51625bc2"
