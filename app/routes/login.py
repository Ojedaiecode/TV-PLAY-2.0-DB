# Arquivo responsável pelas rotas de autenticação (login e logout)
# Desenvolvido para o QG Ojed AI & Code - Coronel Ojed e General Dejo

from flask import Blueprint, request, session, redirect, url_for, flash, render_template, jsonify
from app.services.supabase_service import get_supabase_client
import bcrypt
import os
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criação do Blueprint
login_bp = Blueprint('login', __name__)

# Tenta inicializar o cliente Supabase
try:
    supabase = get_supabase_client()
    if not supabase:
        logger.error("Falha ao inicializar cliente Supabase")
except Exception as e:
    logger.error(f"Erro ao conectar com Supabase: {str(e)}")
    supabase = None

def gerar_hash_senha(senha):
    """
    Gera um hash bcrypt para a senha fornecida
    """
    try:
        return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except Exception as e:
        logger.error(f"Erro ao gerar hash: {str(e)}")
        return None

def verificar_senha(senha_digitada, hash_senha):
    """
    Verifica se a senha digitada corresponde ao hash armazenado
    Aceita tanto hashes $2a$ quanto $2b$
    """
    try:
        logger.info(f"Tentando verificar senha. Hash armazenado: {hash_senha[:20]}...")
        senha_bytes = senha_digitada.encode('utf-8')
        hash_bytes = hash_senha.encode('utf-8')
        
        # Tenta verificar normalmente primeiro
        try:
            return bcrypt.checkpw(senha_bytes, hash_bytes)
        except Exception as e1:
            logger.warning(f"Primeira tentativa de verificação falhou: {str(e1)}")
            
            # Se falhou e o hash começa com $2a$, tenta converter para $2b$
            if hash_senha.startswith('$2a$'):
                try:
                    hash_modificado = hash_senha.replace('$2a$', '$2b$', 1)
                    hash_bytes_mod = hash_modificado.encode('utf-8')
                    return bcrypt.checkpw(senha_bytes, hash_bytes_mod)
                except Exception as e2:
                    logger.error(f"Tentativa de verificação com hash modificado falhou: {str(e2)}")
                    return False
            return False
            
    except Exception as e:
        logger.error(f"Erro ao verificar senha: {str(e)}")
        return False

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Rota GET para teste
    if request.method == 'GET':
        return jsonify({"message": "Rota de login funcionando no backend!"})
    
    try:
        # Recebe os dados do formulário
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('main.index'))

        # Verifica se o Supabase está configurado
        if not supabase:
            logger.error("Supabase não está configurado")
            flash('Erro de configuração no servidor.')
            return redirect(url_for('main.index'))

        # Busca o usuário no Supabase
        logger.info(f"Tentando login para email: {email}")
        response = supabase.table('usuario_admin') \
            .select('id, nome, email, senha, avatar_url') \
            .eq('email', email) \
            .execute()

        # Verifica se encontrou o usuário
        if response.data and len(response.data) > 0:
            user = response.data[0]
            logger.info(f"Usuário encontrado: {user['email']}")
            
            # Verifica a senha usando bcrypt
            if verificar_senha(senha, user['senha']):
                logger.info("Senha verificada com sucesso")
                # Cria a sessão do usuário (removendo a senha dos dados da sessão)
                session['user'] = {
                    'id': user['id'],
                    'nome': user['nome'],
                    'email': user['email'],
                    'avatar_url': user['avatar_url']
                }
                
                return redirect(url_for('home_bp.home'))
            else:
                logger.warning("Falha na verificação da senha")
                flash('Email ou senha incorretos.')
                return redirect(url_for('main.index'))
        else:
            logger.warning(f"Usuário não encontrado para o email: {email}")
            flash('Email ou senha incorretos.')
            return redirect(url_for('main.index'))

    except Exception as e:
        logger.error(f"Erro no processo de login: {str(e)}")
        flash('Erro ao realizar login. Tente novamente.')
        return redirect(url_for('main.index'))

@login_bp.route('/logout')
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
        supabase.table('usuario_admin') \
            .update({'senha': senha_hash}) \
            .eq('id', user_id) \
            .execute()
        return True
    except Exception:
        return False 