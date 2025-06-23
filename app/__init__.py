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
    try:
        # Cria a aplicação Flask
        app = Flask(__name__)
        
        # Configuração do CORS para permitir tanto o site público quanto o painel admin
        CORS(app,
            resources={
                # Configuração para rotas públicas
                r"/auth/*": {
                    "origins": [
                        "https://tvplaydastorcidas.com",
                        "https://www.tvplaydastorcidas.com"
                    ],
                    "methods": ["GET", "POST", "OPTIONS"],
                    "allow_headers": ["Content-Type", "Authorization"],
                    "supports_credentials": True
                },
                # Configuração para o painel admin
                r"/*": {
                    "origins": ["*"],  # Permite temporariamente todas as origens para o painel admin
                    "methods": ["GET", "POST", "OPTIONS"],
                    "allow_headers": ["Content-Type", "Authorization"],
                    "supports_credentials": True
                }
            }
        )
        
        # Configurações da aplicação
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Alterado para Lax para permitir redirecionamentos
        
        # Registra todos os blueprints necessários
        from app.routes.public_auth import public_auth_bp
        from app.routes.main import main_bp
        from app.routes.login import login_bp
        from app.routes.home import home_bp
        from app.routes.avatar import avatar_bp
        from app.routes.usuarios_gratis import usuarios_gratis_bp
        from app.routes.add_user_gratis_view import add_user_gratis_bp
        
        app.register_blueprint(public_auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(login_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(avatar_bp)
        app.register_blueprint(usuarios_gratis_bp)
        app.register_blueprint(add_user_gratis_bp)
        
        # Rota principal do painel admin
        @app.route('/')
        def index():
            return render_template('index.html')
        
        # Rota de healthcheck
        @app.route('/health')
        def health_check():
            return jsonify({
                'status': 'healthy',
                'message': 'API TV Play das Torcidas está operacional'
            })
        
        return app
        
    except Exception as e:
        print(f"Erro crítico na inicialização do app: {str(e)}")
        raise  