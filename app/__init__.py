"""
Inicialização da aplicação Flask
Desenvolvido para o QG Ojed AI & Code - General Dejo

Este módulo é responsável por:
1. Criar e configurar a aplicação Flask
2. Registrar os blueprints
3. Configurar middlewares e extensões
4. Inicializar serviços externos
"""

from flask import Flask, jsonify, render_template
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
    
    # Configuração do CORS para permitir acesso ao painel admin
    CORS(app)
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
    
    # Registra os blueprints necessários
    from app.routes.main import main_bp
    from app.routes.login import login_bp
    from app.routes.home import home_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(home_bp)
    
    # Rota de healthcheck
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'API TV Play das Torcidas está operacional'
        })
    
    return app 