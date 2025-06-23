"""
Inicialização da aplicação Flask
Desenvolvido para o QG Ojed AI & Code - General Dejo

Este módulo é responsável por:
1. Criar e configurar a aplicação Flask
2. Registrar os blueprints
3. Configurar middlewares e extensões
4. Inicializar serviços externos
"""

from flask import Flask, request, make_response
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
    
    # Configuração do CORS conforme especificado pelo General
    CORS(
        app, 
        resources={r"/*": {"origins": "https://tvplaydastorcidas.com"}}, 
        supports_credentials=True
    )
    
    # Handler manual para requisições OPTIONS
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = 'https://tvplaydastorcidas.com'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.status_code = 200
            return response
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    
    # Registra os blueprints
    from app.routes.public_auth import public_auth_bp
    app.register_blueprint(public_auth_bp)
    
    return app  