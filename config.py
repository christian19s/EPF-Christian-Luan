import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "images")
SECRET_KEY = SECRET_KEY = os.environ.get("SECRET_KEY.txt")


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
