# Arquivo responsável pelas rotas de autenticação (login e logout)
# Desenvolvido para o QG Ojed AI & Code - Coronel Ojed e General Dejo

from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from app.config import supabase
import bcrypt

# Criação do Blueprint
auth = Blueprint('auth', __name__)

def gerar_hash_senha(senha):
    """
    Gera um hash bcrypt para a senha fornecida
    """
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_senha(senha_digitada, hash_senha):
    """
    Verifica se a senha digitada corresponde ao hash armazenado
    """
    try:
        return bcrypt.checkpw(
            senha_digitada.encode('utf-8'),
            hash_senha.encode('utf-8')
        )
    except Exception:
        return False

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
            .select('id, nome, email, senha, avatar_url') \
            .eq('email', email) \
            .execute()

        # Verifica se encontrou o usuário
        if response.data and len(response.data) > 0:
            user = response.data[0]
            
            # Verifica a senha usando bcrypt
            if verificar_senha(senha, user['senha']):
                # Cria a sessão do usuário (removendo a senha dos dados da sessão)
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

# Função auxiliar para atualizar senha de usuário existente
def atualizar_senha_usuario(user_id, nova_senha):
    """
    Atualiza a senha de um usuário existente com hash bcrypt
    Usar apenas em script de migração ou painel administrativo
    """
    try:
        senha_hash = gerar_hash_senha(nova_senha)
        supabase.table('user_admin') \
            .update({'senha': senha_hash}) \
            .eq('id', user_id) \
            .execute()
        return True
    except Exception:
        return False 