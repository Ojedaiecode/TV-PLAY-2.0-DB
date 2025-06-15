from flask import Flask
from app.config import SECRET_KEY, FLASK_ENV

def create_app():
    app = Flask(__name__)
    
    # Configuração da aplicação
    app.config.update(
        SECRET_KEY=SECRET_KEY,
        ENV=FLASK_ENV
    )

    # Configurações de segurança da sessão
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = True

    # Importa e registra blueprints de rotas
    from .routes.main import main_bp    # Rotas públicas (index)
    from .routes.login import auth      # Rotas de autenticação
    from .routes.home import home_bp    # Rotas protegidas (dashboard)
    from .routes.avatar import avatar_bp # Rotas de upload de avatar

    # Registro dos blueprints
    app.register_blueprint(main_bp)     # Rotas principais
    app.register_blueprint(auth)        # Rotas de autenticação
    app.register_blueprint(home_bp)     # Rotas do dashboard
    app.register_blueprint(avatar_bp)   # Rotas de avatar

    return app  