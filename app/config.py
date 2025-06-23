"""
Configurações da aplicação Flask
Desenvolvido para o QG Ojed AI & Code - General Dejo

Este módulo centraliza todas as configurações da aplicação,
incluindo variáveis de ambiente, conexões com serviços externos
e outras configurações globais.
"""

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY são obrigatórias. "
        "Certifique-se de que estão configuradas no ambiente ou no arquivo .env"
    )

# Configurações da aplicação
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
FLASK_ENV = os.getenv('FLASK_ENV', 'production')  # Default para production 