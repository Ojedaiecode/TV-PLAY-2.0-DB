from flask import Flask
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuração da chave secreta para sessões
    app.secret_key = os.getenv('SECRET_KEY', 'uma-chave-secreta-temporaria')

    # Importa e registra blueprints de rotas
    from .routes.main import main_bp
    from .routes.login import auth
    from .routes.home import home_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth)
    app.register_blueprint(home_bp)

    return app 