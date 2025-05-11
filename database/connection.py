import psycopg2
from dotenv import load_dotenv
import os

#carrega as variaveis de ambiente do arquivo .env
load_dotenv()

try:
    # Conexão com o banco de dados PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )  
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")


# Criação de um cursor para executar comandos SQL
cursor = conn.cursor()

# Execute uma consulta simples
cursor.execute("SELECT version();")

# Obtenha o resultado
result = cursor.fetchone()
print(f"Conexão bem-sucedida: {result}")

# Feche o cursor e a conexão
cursor.close()
conn.close()