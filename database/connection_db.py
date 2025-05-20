from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

#carrega as variaveis de ambiente do arquivo .env
load_dotenv()

# Configurações do banco de dados
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:port/financial_db"

