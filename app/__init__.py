"""
Inicialização da aplicação Flask
Desenvolvido para o QG Ojed AI & Code - General Dejo

Este módulo é responsável por:
1. Criar e configurar a aplicação Flask
2. Registrar os blueprints
3. Configurar middlewares e extensões
4. Inicializar serviços externos
"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

def create_app():
    """
    Cria e configura a aplicação Flask
    
    Returns:
        app: Aplicação Flask configurada
    """
    # Cria a aplicação Flask
    app = Flask(__name__)
    
    # Configuração do CORS
    CORS(app, 
         resources={
             r"/auth/*": {
                 "origins": [
                     "https://tvplaydastorcidas.com",
                     "https://www.tvplaydastorcidas.com"
                 ],
                 "supports_credentials": True,
                 "allow_headers": ["Content-Type"],
                 "methods": ["POST", "OPTIONS"]
             }
         })
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    
    # Registra os blueprints
    from app.routes.public_auth import public_auth_bp
    app.register_blueprint(public_auth_bp)
    
    return app  