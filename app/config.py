"""
Configurações da aplicação Flask
Desenvolvido para o QG Ojed AI & Code - General Dejo

Este módulo centraliza todas as configurações da aplicação,
incluindo variáveis de ambiente, conexões com serviços externos
e outras configurações globais.
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Supabase
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    raise ValueError(
        "Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY são obrigatórias. "
        "Certifique-se de que estão configuradas no ambiente ou no arquivo .env"
    )

# Inicializa o cliente Supabase
supabase = create_client(supabase_url, supabase_key)

# Configurações da aplicação
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
FLASK_ENV = os.getenv('FLASK_ENV', 'production')  # Default para production 