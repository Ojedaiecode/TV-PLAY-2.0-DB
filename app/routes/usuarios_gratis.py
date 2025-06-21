"""
Blueprint para gerenciamento de rotas relacionadas aos usuários gratuitos

Rotas implementadas:
- /teste: Rota de teste para verificar se o blueprint está funcional
- /login: Rota de autenticação de usuários gratuitos (POST)
- /register: Rota de cadastro de usuários gratuitos (POST)
- /listar_usuarios: Rota para listar usuários gratuitos (GET)
- /atualizar_usuario: Rota para atualizar dados de usuário (PUT)
- /deletar_usuario: Rota para deletar usuário (DELETE)
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.services.supabase_service import get_supabase_client
from datetime import datetime

# Criação do Blueprint para usuários grátis
usuarios_gratis_bp = Blueprint('usuarios_gratis', __name__)

@usuarios_gratis_bp.route('/teste')
def teste_rota():
    """Rota de teste para verificar se o blueprint está funcional"""
    return {'status': 'ok', 'message': 'Blueprint de usuários grátis está funcionando!'}

@usuarios_gratis_bp.route('/login', methods=['POST'])
def login():
    """
    Rota de autenticação para usuários gratuitos
    
    Recebe:
        - email: Email do usuário
        - senha: Senha do usuário
    
    Retorna:
        - Sucesso: {'status': 'success', 'message': 'Login realizado com sucesso'}
        - Erro: {'status': 'error', 'message': 'Usuário ou senha inválidos'}
    """
    try:
        # Obtém os dados do request
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        # Valida se os campos foram enviados
        if not email or not senha:
            return jsonify({
                'status': 'error',
                'message': 'Email e senha são obrigatórios'
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
                'message': 'Usuário ou senha inválidos'
            }), 401

        usuario = response.data[0]

        # Verifica se a senha está correta
        if not check_password_hash(usuario['senha'], senha):
            return jsonify({
                'status': 'error',
                'message': 'Usuário ou senha inválidos'
            }), 401

        # Login realizado com sucesso
        return jsonify({
            'status': 'success',
            'message': 'Login realizado com sucesso'
        })

    except Exception as e:
        # Log do erro (em produção, usar um logger apropriado)
        print(f'Erro no login: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Erro ao realizar login'
        }), 500

@usuarios_gratis_bp.route('/register', methods=['POST'])
def register():
    """
    Rota de cadastro para usuários gratuitos
    
    Recebe:
        - nome: Nome completo do usuário
        - email: Email do usuário
        - celular: Número de celular
        - senha: Senha do usuário
    
    Retorna:
        - Sucesso (201): {'status': 'success', 'message': 'Usuário cadastrado com sucesso'}
        - Erro (409): {'status': 'error', 'message': 'Email já cadastrado'}
        - Erro (400): {'status': 'error', 'message': 'Campos obrigatórios não enviados'}
        - Erro (500): {'status': 'error', 'message': 'Erro ao realizar cadastro'}
    """
    try:
        # Obtém os dados do request
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        celular = data.get('celular')
        senha = data.get('senha')

        # Valida se todos os campos obrigatórios foram enviados
        if not all([nome, email, celular, senha]):
            return jsonify({
                'status': 'error',
                'message': 'Todos os campos são obrigatórios'
            }), 400

        # Obtém o cliente do Supabase
        supabase = get_supabase_client()

        # Verifica se o email já está cadastrado
        response = supabase.table('usuarios_gratis') \
            .select('id') \
            .eq('email', email) \
            .execute()

        if response.data and len(response.data) > 0:
            return jsonify({
                'status': 'error',
                'message': 'Email já cadastrado'
            }), 409

        # Prepara os dados para inserção
        novo_usuario = {
            'nome': nome,
            'email': email,
            'celular': celular,
            'senha': generate_password_hash(senha),
            'status': 'ativo',
            'data_cadastro': datetime.utcnow().isoformat(),
            'ip_cadastro': request.remote_addr if request.remote_addr else None
        }

        # Insere o novo usuário
        response = supabase.table('usuarios_gratis') \
            .insert(novo_usuario) \
            .execute()

        # Verifica se a inserção foi bem sucedida
        if not response.data or len(response.data) == 0:
            raise Exception('Erro ao inserir usuário no banco')

        # Retorna sucesso
        return jsonify({
            'status': 'success',
            'message': 'Usuário cadastrado com sucesso'
        }), 201

    except Exception as e:
        # Log do erro (em produção, usar um logger apropriado)
        print(f'Erro no cadastro: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Erro ao realizar cadastro'
        }), 500

@usuarios_gratis_bp.route('/listar_usuarios', methods=['GET'])
def listar_usuarios():
    """
    Rota para listar todos os usuários gratuitos cadastrados
    
    Retorna:
        - Sucesso (200): {
            'status': 'success',
            'usuarios': [
                {
                    'id': 'uuid',
                    'nome': 'string',
                    'email': 'string',
                    'status': 'string',
                    'data_cadastro': 'datetime'
                },
                ...
            ]
        }
        - Erro (500): {'status': 'error', 'message': 'Erro ao listar usuários'}
    """
    try:
        # Obtém o cliente do Supabase
        supabase = get_supabase_client()

        # Busca os usuários, selecionando apenas os campos necessários
        response = supabase.table('usuarios_gratis') \
            .select('id, nome, email, status, data_cadastro') \
            .execute()

        # Verifica se a consulta foi bem sucedida
        if not response.data:
            # Se não houver dados, retorna lista vazia
            return jsonify({
                'status': 'success',
                'usuarios': []
            })

        # Retorna a lista de usuários
        return jsonify({
            'status': 'success',
            'usuarios': response.data
        })

    except Exception as e:
        # Log do erro (em produção, usar um logger apropriado)
        print(f'Erro ao listar usuários: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Erro ao listar usuários'
        }), 500 

@usuarios_gratis_bp.route('/atualizar_usuario', methods=['PUT'])
def atualizar_usuario():
    """
    Rota para atualizar dados de um usuário gratuito
    
    Recebe:
        - id: UUID do usuário (obrigatório)
        - nome: Novo nome (opcional)
        - email: Novo email (opcional)
        - celular: Novo celular (opcional)
        - status: Novo status (opcional) - valores: ativo, inativo, bloqueado
    
    Retorna:
        - Sucesso (200): {'status': 'success', 'message': 'Dados atualizados com sucesso'}
        - Erro (404): {'status': 'error', 'message': 'Usuário não encontrado'}
        - Erro (400): {'status': 'error', 'message': 'ID do usuário é obrigatório'}
        - Erro (500): {'status': 'error', 'message': 'Erro ao atualizar dados'}
    """
    try:
        # Obtém os dados do request
        data = request.get_json()
        
        # Verifica se o ID foi enviado
        user_id = data.get('id')
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'ID do usuário é obrigatório'
            }), 400

        # Obtém o cliente do Supabase
        supabase = get_supabase_client()

        # Verifica se o usuário existe
        check_user = supabase.table('usuarios_gratis') \
            .select('id') \
            .eq('id', user_id) \
            .execute()

        if not check_user.data or len(check_user.data) == 0:
            return jsonify({
                'status': 'error',
                'message': 'Usuário não encontrado'
            }), 404

        # Prepara os dados para atualização
        update_data = {}
        
        # Adiciona apenas os campos que foram enviados
        if 'nome' in data:
            update_data['nome'] = data['nome']
        if 'email' in data:
            update_data['email'] = data['email']
        if 'celular' in data:
            update_data['celular'] = data['celular']
        if 'status' in data:
            # Valida o status
            status = data['status'].lower()
            if status not in ['ativo', 'inativo', 'bloqueado']:
                return jsonify({
                    'status': 'error',
                    'message': 'Status inválido'
                }), 400
            update_data['status'] = status

        # Se não há dados para atualizar
        if not update_data:
            return jsonify({
                'status': 'success',
                'message': 'Nenhum dado para atualizar'
            })

        # Atualiza os dados do usuário
        response = supabase.table('usuarios_gratis') \
            .update(update_data) \
            .eq('id', user_id) \
            .execute()

        # Verifica se a atualização foi bem sucedida
        if not response.data or len(response.data) == 0:
            raise Exception('Erro ao atualizar dados no banco')

        # Retorna sucesso
        return jsonify({
            'status': 'success',
            'message': 'Dados atualizados com sucesso'
        })

    except Exception as e:
        # Log do erro (em produção, usar um logger apropriado)
        print(f'Erro ao atualizar usuário: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Erro ao atualizar dados'
        }), 500 

@usuarios_gratis_bp.route('/deletar_usuario', methods=['DELETE'])
def deletar_usuario():
    """
    Rota para deletar um usuário gratuito do sistema
    
    Recebe:
        - id: UUID do usuário (obrigatório)
    
    Retorna:
        - Sucesso (200): {'status': 'success', 'message': 'Usuário deletado com sucesso'}
        - Erro (404): {'status': 'error', 'message': 'Usuário não encontrado'}
        - Erro (400): {'status': 'error', 'message': 'ID do usuário é obrigatório'}
        - Erro (500): {'status': 'error', 'message': 'Erro ao deletar usuário'}
    """
    try:
        # Obtém os dados do request
        data = request.get_json()
        
        # Verifica se o ID foi enviado
        user_id = data.get('id')
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'ID do usuário é obrigatório'
            }), 400

        # Obtém o cliente do Supabase
        supabase = get_supabase_client()

        # Verifica se o usuário existe
        check_user = supabase.table('usuarios_gratis') \
            .select('id') \
            .eq('id', user_id) \
            .execute()

        if not check_user.data or len(check_user.data) == 0:
            return jsonify({
                'status': 'error',
                'message': 'Usuário não encontrado'
            }), 404

        # Realiza a deleção física do usuário
        response = supabase.table('usuarios_gratis') \
            .delete() \
            .eq('id', user_id) \
            .execute()

        # Verifica se a deleção foi bem sucedida
        if not response.data or len(response.data) == 0:
            raise Exception('Erro ao deletar usuário no banco')

        # Retorna sucesso
        return jsonify({
            'status': 'success',
            'message': 'Usuário deletado com sucesso'
        })

    except Exception as e:
        # Log do erro (em produção, usar um logger apropriado)
        print(f'Erro ao deletar usuário: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Erro ao deletar usuário'
        }), 500 