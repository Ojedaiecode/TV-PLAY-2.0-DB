# Arquivo responsável pela rota de renderização do template add-user-gratis.html
# Desenvolvido para o QG Ojed AI & Code

from flask import Blueprint, render_template, session, redirect, url_for

# Criação do Blueprint
add_user_gratis_bp = Blueprint('add_user_gratis', __name__)

@add_user_gratis_bp.route('/add-user-gratis')
def add_user_gratis():
    # Verifica se existe uma sessão ativa
    if 'user' in session:
        return render_template('add-user-gratis.html')
    
    # Se não houver sessão, redireciona para a página inicial
    return redirect(url_for('main.index')) 