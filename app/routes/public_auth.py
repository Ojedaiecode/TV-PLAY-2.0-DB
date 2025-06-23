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

from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import check_password_hash
from app.services.supabase_service import get_supabase_client
from datetime import datetime

# Criação do Blueprint com prefixo /auth
public_auth_bp = Blueprint('public_auth', __name__, url_prefix='/auth')

@public_auth_bp.route('/login', methods=['POST', 'OPTIONS'])
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
    # Tratamento especial para requisições OPTIONS (preflight)
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'https://tvplaydastorcidas.com')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    try:
        # Obtém os dados do request
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        # Valida se os campos obrigatórios foram enviados
        if not email or not senha:
            response = jsonify({
                'status': 'error',
                'message': 'Campos obrigatórios não enviados'
            })
            response.headers.add('Access-Control-Allow-Origin', 'https://tvplaydastorcidas.com')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 400

        # Obtém o cliente do Supabase
        supabase = get_supabase_client()

        # Busca o usuário pelo email
        response = supabase.table('usuarios_gratis') \
            .select('*') \
            .eq('email', email) \
            .execute()

        # Verifica se encontrou o usuário
        if not response.data or len(response.data) == 0:
            response = jsonify({
                'status': 'error',
                'message': 'Email ou senha inválidos'
            })
            response.headers.add('Access-Control-Allow-Origin', 'https://tvplaydastorcidas.com')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 401

        usuario = response.data[0]

        # Verifica se a senha está correta
        if not check_password_hash(usuario['senha'], senha):
            response = jsonify({
                'status': 'error',
                'message': 'Email ou senha inválidos'
            })
            response.headers.add('Access-Control-Allow-Origin', 'https://tvplaydastorcidas.com')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 401

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
        response = jsonify({
            'status': 'success',
            'message': 'Login realizado com sucesso'
        })
        response.headers.add('Access-Control-Allow-Origin', 'https://tvplaydastorcidas.com')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    except Exception as e:
        # Log do erro (em produção, usar um logger apropriado)
        print(f'Erro no login público: {str(e)}')
        response = jsonify({
            'status': 'error',
            'message': 'Erro ao realizar login'
        })
        response.headers.add('Access-Control-Allow-Origin', 'https://tvplaydastorcidas.com')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response, 500 