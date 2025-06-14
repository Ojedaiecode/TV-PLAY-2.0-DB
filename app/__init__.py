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
    from .routes.main import main_bp
    from .routes.login import auth
    from .routes.home import home_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth)
    app.register_blueprint(home_bp)

    return app 