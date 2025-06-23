"""
Serviço para gerenciamento de conexões e operações com Supabase

Este módulo centraliza a conexão com o Supabase e fornece funções
genéricas para serem utilizadas em qualquer rota que precise
interagir com o banco de dados.
"""
from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY

def get_supabase_client():
    """
    Cria e retorna um cliente configurado do Supabase.
    
    Returns:
        Client: Cliente do Supabase configurado com as credenciais do ambiente
    """
    return create_client(SUPABASE_URL, SUPABASE_KEY) 