"""
Blueprint responsável pelas rotas de autenticação pública
Desenvolvido para o QG Ojed AI & Code - General Dejo

Este módulo gerencia todas as rotas da API pública que serão consumidas
pelo frontend público do projeto, incluindo:
- Login público
- Autenticação
- Verificação de IP
- Gerenciamento de sessão
e outras funcionalidades relacionadas à autenticação pública.

Importante: Este blueprint é exclusivo para o site público,
não tendo relação com o painel administrativo.
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.services.supabase_service import get_supabase_client
from datetime import datetime

# Criação do Blueprint com prefixo /auth
public_auth_bp = Blueprint('public_auth', __name__, url_prefix='/auth')

@public_auth_bp.route('/login', methods=['POST'])
def login():
    """
    Rota pública de login para usuários gratuitos
    
    Recebe:
        - email: Email do usuário
        - senha: Senha do usuário
    
    Retorna:
        - Sucesso (200): {'status': 'success', 'message': 'Login realizado com sucesso'}
        - Erro (400): {'status': 'error', 'message': 'Campos obrigatórios não enviados'}
        - Erro (401): {'status': 'error', 'message': 'Email ou senha inválidos'}
        - Erro (500): {'status': 'error', 'message': 'Erro ao realizar login'}
    """
    try:
        # Obtém os dados do request
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        # Valida se os campos obrigatórios foram enviados
        if not email or not senha:
            return jsonify({
                'status': 'error',
                'message': 'Campos obrigatórios não enviados'
            }), 400

        # Obtém o cliente do Supabase
        supabase = get_supabase_client()

        # Busca o usuário pelo email
        response = supabase.table('usuarios_gratis') \
            .select('*') \
            .eq('email', email) \
            .execute()

        # Verifica se encontrou o usuário
        if not response.data or len(response.data) == 0:
            return jsonify({
                'status': 'error',
                'message': 'Email ou senha inválidos'
            }), 401

        usuario = response.data[0]

        # Verifica se a senha está correta
        if not check_password_hash(usuario['senha'], senha):
            return jsonify({
                'status': 'error',
                'message': 'Email ou senha inválidos'
            }), 401

        # Prepara os dados para atualização
        update_data = {
            'ultimo_acesso': datetime.utcnow().isoformat(),
            'ultimo_ip': request.remote_addr,
            'quantidade_acessos': (usuario.get('quantidade_acessos', 0) or 0) + 1
        }

        # Atualiza os dados do usuário
        supabase.table('usuarios_gratis') \
            .update(update_data) \
            .eq('id', usuario['id']) \
            .execute()

        # Login realizado com sucesso
        return jsonify({
            'status': 'success',
            'message': 'Login realizado com sucesso'
        })

    except Exception as e:
        # Log do erro (em produção, usar um logger apropriado)
        print(f'Erro no login público: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Erro ao realizar login'
        }), 500 