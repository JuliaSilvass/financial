# models/user.py

from sqlalchemy import Column, Integer, String
from database.connection_db import Base

class User(Base):
    __tablename__ = "usuario"  # nome exato da tabela no banco

    usuario_id = Column(Integer, primary_key=True, index=True)
    usuario_nome = Column(String, nullable=False)
    usuario_email = Column(String, unique=True, index=True, nullable=False)
    usuario_senha_hash = Column(String, nullable=False)

    def __init__(self, nome=None, email=None, password=None):
        self.usuario_nome = nome
        self.usuario_email = email
        self.usuario_senha_hash = password

    def __repr__(self):
        return f"User(id={self.usuario_id}, nome={self.usuario_nome}, email={self.usuario_email})"

    @property
    def nome(self):
        return self.usuario_nome

    @nome.setter
    def nome(self, valor):
        self.usuario_nome = valor

    @property
    def email(self):
        return self.usuario_email

    @email.setter
    def email(self, valor):
        self.usuario_email = valor
