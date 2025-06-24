"""
Serviço para gerenciamento de conexões e operações com Supabase

Este módulo centraliza a conexão com o Supabase e fornece funções
genéricas para serem utilizadas em qualquer rota que precise
interagir com o banco de dados.
"""
from supabase import create_client
import os

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
            print("[AVISO] Credenciais do Supabase não encontradas")
            return None
            
        return create_client(url, key)
    except Exception as e:
        print(f"[ERRO] Falha ao conectar com Supabase: {str(e)}")
        return None 