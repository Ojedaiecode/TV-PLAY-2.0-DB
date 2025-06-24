"""
Inicialização da aplicação Flask
Desenvolvido para o QG Ojed AI & Code - General Dejo

Este módulo é responsável por:
1. Criar e configurar a aplicação Flask
2. Registrar os blueprints
3. Configurar middlewares e extensões
4. Inicializar serviços externos
"""

from flask import Flask, render_template

def create_app():
    """
    Cria e configura a aplicação Flask
    
    Returns:
        app: Aplicação Flask configurada
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    
    @app.route('/')
    def index():
        return render_template('index.html')
        
    return app 