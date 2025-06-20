import os


class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Configurações do servidor
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 8080))
    DEBUG = os.environ.get("DEBUG", "True") == "True"
    RELOADER = os.environ.get("RELOADER", "True") == "True"

    # Paths
    TEMPLATE_PATH = os.path.join(BASE_DIR, "views")
    STATIC_PATH = os.path.join(BASE_DIR, "static")
    DATA_PATH = os.path.join(BASE_DIR, "data")

    # Outras configurações
    SECRET_KEY = "sua-chave-secreta-aqui"
