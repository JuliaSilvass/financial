from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base 
from dotenv import load_dotenv
import os

#carrega as variaveis de ambiente do arquivo .env
load_dotenv()

# carrega as variaveis de ambiente do arquivo .env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Configurações do banco de dados
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criar engine (responsável pela conexão)
engine = create_engine(DATABASE_URL, echo=True)

# Criar sessão (responsável pelas operações no banco)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos (tabelas)
Base = declarative_base()



def test_connection():
    try:
        # Tenta conectar ao banco de dados
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()
            print("Conexão bem-sucedida ao banco de dados!")
            print(f"Versão do banco de dados: {version[0]}")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")