# Arquivo responsável pelo upload e gerenciamento de avatares
# Desenvolvido para o QG Ojed AI & Code

from flask import Blueprint, request, session, jsonify
from app.config import supabase
import os
from werkzeug.utils import secure_filename

# Criação do Blueprint
avatar_bp = Blueprint('avatar_bp', __name__)

# Extensões permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and \
           filename.lower().split('.')[-1] in ALLOWED_EXTENSIONS

@avatar_bp.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    try:
        # Verifica se existe sessão ativa
        if 'user' not in session:
            return jsonify({'error': 'Usuário não autenticado'}), 401

        # Verifica se foi enviado um arquivo
        if 'avatar' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400

        file = request.files['avatar']

        # Verifica se um arquivo foi selecionado
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

        # Verifica se é uma extensão permitida
        if not allowed_file(file.filename):
            return jsonify({'error': 'Formato de arquivo não permitido. Use PNG, JPG ou JPEG'}), 400

        # Verifica o tamanho do arquivo
        file_content = file.read()
        file.seek(0)  # Reset do ponteiro do arquivo
        if len(file_content) > MAX_FILE_SIZE:
            return jsonify({'error': 'Arquivo muito grande. Máximo permitido: 5MB'}), 400

        try:
            # Gera o nome do arquivo baseado no ID do usuário
            filename = secure_filename(file.filename)
            new_filename = f"{session['user']['id']}_{filename}"
            file_path = f"avatars/{new_filename}"

            # Tenta excluir avatar anterior se existir
            try:
                old_avatar_url = session['user'].get('avatar_url', '')
                if old_avatar_url and 'avatars/' in old_avatar_url:
                    old_file_path = old_avatar_url.split('avatars/')[-1]
                    supabase.storage.from_('avatars').remove([old_file_path])
            except Exception:
                # Ignora erros ao tentar remover avatar antigo
                pass

            # Upload do novo arquivo
            supabase.storage.from_('avatars').upload(
                file_path,
                file_content,
                file_options={"content-type": file.content_type}
            )

            # Obtém a URL pública do arquivo
            file_url = supabase.storage.from_('avatars').get_public_url(file_path)

            # Atualiza a URL do avatar no banco de dados
            update_result = supabase.table('user_admin') \
                .update({'avatar_url': file_url}) \
                .eq('id', session['user']['id']) \
                .execute()

            if not update_result.data:
                raise Exception('Falha ao atualizar o banco de dados')

            # Atualiza a sessão
            session['user']['avatar_url'] = file_url

            return jsonify({
                'message': 'Avatar atualizado com sucesso',
                'avatar_url': file_url
            }), 200

        except Exception as e:
            return jsonify({
                'error': 'Erro ao fazer upload do avatar. Verifique as permissões do bucket ou tente novamente.',
                'details': str(e)
            }), 500

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500 