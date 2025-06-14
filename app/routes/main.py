# Arquivo responsável pela rota principal (index)
# Desenvolvido para o QG Ojed AI & Code

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Página inicial simples
    return render_template('index.html') 