from flask import Flask
from app.config import SECRET_KEY, FLASK_ENV

def create_app():
    app = Flask(__name__)
    
    # Configuração da aplicação
    app.config.update(
        SECRET_KEY=SECRET_KEY,
        ENV=FLASK_ENV
    )

    # Importa e registra blueprints de rotas
    from .routes.main import main_bp    # Rotas públicas (index)
    from .routes.login import auth      # Rotas de autenticação
    from .routes.home import home_bp    # Rotas protegidas (dashboard)

    # Registro dos blueprints
    app.register_blueprint(main_bp)     # Rotas principais
    app.register_blueprint(auth)        # Rotas de autenticação
    app.register_blueprint(home_bp)     # Rotas do dashboard

    return app 