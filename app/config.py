import os
from supabase import create_client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente apenas em ambiente de desenvolvimento
if os.getenv('FLASK_ENV') != 'production':
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

# Outras configurações da aplicação
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
FLASK_ENV = os.getenv('FLASK_ENV', 'development') 