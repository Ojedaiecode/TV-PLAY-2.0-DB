"""
Serviço para gerenciamento de conexões e operações com Supabase

Este módulo centraliza a conexão com o Supabase e fornece funções
genéricas para serem utilizadas em qualquer rota que precise
interagir com o banco de dados.
"""
from supabase import create_client
import os
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_supabase_client():
    """
    Cria e retorna um cliente configurado do Supabase.
    Se as credenciais não estiverem disponíveis, retorna None.
    
    Returns:
        Client: Cliente do Supabase configurado ou None se não configurado
    """
    try:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            logger.error("Credenciais do Supabase não encontradas. URL: %s, KEY: %s", 
                        bool(url), bool(key))
            return None
        
        # Tenta criar o cliente e fazer uma conexão de teste
        client = create_client(url, key)
        
        # Testa a conexão fazendo uma query simples
        try:
            client.table('usuario_admin').select("count", "exact").execute()
            logger.info("Conexão com Supabase estabelecida com sucesso")
            return client
        except Exception as table_error:
            logger.error("Erro ao acessar tabela usuario_admin: %s", str(table_error))
            return None
            
    except Exception as e:
        logger.error("Falha ao conectar com Supabase: %s", str(e))
        return None 