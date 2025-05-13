import psycopg2
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#carrega as variaveis de ambiente do arquivo .env
load_dotenv()

def connect_to_database():
    """
    Função para conectar ao banco de dados PostgreSQL.
    """
    try:
        # Conexão com o banco de dados PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )  

        logging.info("Conexão com o banco de dados estabelecida com sucesso.")

        # Comandos para excecutar no banco de dados
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        logging.info(f"Versão do banco de dados: {result}")

    except Exception as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}", exc_info=True)
        return None

    return conn