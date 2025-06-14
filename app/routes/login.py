# Arquivo responsável pelas rotas de autenticação (login e logout)
# Desenvolvido para o QG Ojed AI & Code - Coronel Ojed e General Dejo

from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from app.config import supabase

# Criação do Blueprint
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    try:
        # Recebe os dados do formulário
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('main.index'))

        # Consulta o usuário no Supabase
        response = supabase.table('user_admin') \
            .select('id, nome, email, avatar_url') \
            .eq('email', email) \
            .eq('senha', senha) \
            .execute()

        # Verifica se encontrou o usuário
        if response.data and len(response.data) > 0:
            user = response.data[0]
            
            # Cria a sessão do usuário
            session['user'] = {
                'id': user['id'],
                'nome': user['nome'],
                'email': user['email'],
                'avatar_url': user['avatar_url']
            }
            
            return redirect(url_for('home_bp.home'))
        else:
            flash('Email ou senha incorretos.')
            return redirect(url_for('main.index'))

    except Exception as e:
        flash('Erro ao realizar login. Tente novamente.')
        return redirect(url_for('main.index'))

@auth.route('/logout')
def logout():
    try:
        # Limpa a sessão (funciona mesmo se a sessão não existir)
        session.clear()
    except Exception:
        # Se houver qualquer erro, ignora e continua o logout
        pass
    
    # Redireciona para a página inicial
    return redirect(url_for('main.index')) 