# Arquivo responsável pela rota do Dashboard (home.html)
# Inclui proteção de acesso via sessão
# Criado sob comando do General Dejo e Coronel Ojed – QG Ojed AI & Code

from flask import Blueprint, render_template, session, redirect, url_for

# Criação do Blueprint
home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/home')
def home():
    # Verifica se existe uma sessão ativa
    if 'user' in session:
        return render_template('home.html')
    
    # Se não houver sessão, redireciona para a página inicial
    return redirect(url_for('index')) 