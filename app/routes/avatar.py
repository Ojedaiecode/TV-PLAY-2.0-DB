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

        # Gera o nome do arquivo baseado no ID do usuário
        filename = secure_filename(file.filename)
        new_filename = f"{session['user']['id']}_{filename}"

        # Faz upload para o Supabase Storage
        try:
            # Upload do arquivo para o bucket 'avatars'
            file_path = f"avatars/{new_filename}"
            supabase.storage.from_('avatars').upload(
                file_path,
                file.read(),
                file_options={"content-type": file.content_type}
            )

            # Obtém a URL pública do arquivo
            file_url = supabase.storage.from_('avatars').get_public_url(file_path)

            # Atualiza a URL do avatar no banco de dados
            supabase.table('user_admin') \
                .update({'avatar_url': file_url}) \
                .eq('id', session['user']['id']) \
                .execute()

            # Atualiza a sessão
            session['user']['avatar_url'] = file_url

            return jsonify({
                'message': 'Avatar atualizado com sucesso',
                'avatar_url': file_url
            }), 200

        except Exception as e:
            return jsonify({'error': f'Erro ao fazer upload: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500 