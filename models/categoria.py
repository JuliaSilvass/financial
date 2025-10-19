# models/categoria.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from database.connection_db import Base

class Categoria(Base):
    __tablename__ = "categoria"  # nome exato da tabela no banco

    categoria_id = Column(Integer, primary_key=True, index=True)
    categoria_nome = Column(String(200), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.usuario_id", ondelete="CASCADE"), nullable=False)

    def __init__(self, nome=None, usuario_id=None):
        self.categoria_nome = nome
        self.usuario_id = usuario_id

    def __repr__(self):
        return (
            f"<Categoria(nome='{self.ambiente_nome}', "
            f"usuario_id={self.usuario_id})>"
        )