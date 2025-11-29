import psycopg
from psycopg_pool import ConnectionPool
import os
from contextlib import contextmanager

# Configuração do banco de dados
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "bloodbank")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=10)

@contextmanager
def get_db_connection():
    with pool.connection() as conn:
        yield conn

def read_sql_file(filepath: str) -> str:
    """Lê arquivo SQL de caminho absoluto ou relativo.
    Se relativo, assume que o caminho é relativo ao diretório backend."""
    #Se assegurar que o arquivo e sql
    assert filepath.endswith('.sql'), "Arquivo deve ser um arquivo SQL"
    
    with open(filepath, 'r') as file:
        return file.read()
