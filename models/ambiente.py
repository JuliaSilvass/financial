# models/ambiente.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from database.connection_db import Base

class Ambiente(Base):
    __tablename__ = "ambiente"  # nome exato da tabela no banco

    ambiente_id = Column(Integer, primary_key=True, index=True)
    ambiente_nome = Column(String(200), nullable=False)
    ambiente_descricao = Column(Text, nullable=True)
    ambiente_dt_criacao = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuario.usuario_id", ondelete="CASCADE"), nullable=False)

    def __init__(self, nome=None, descricao=None, usuario_id=None):
        self.ambiente_nome = nome
        self.ambiente_descricao = descricao
        self.usuario_id = usuario_id

    def __repr__(self):
        return (
            f"<Ambiente(id={self.ambiente_id}, nome='{self.ambiente_nome}', "
            f"descricao='{self.ambiente_descricao}', data_criacao={self.ambiente_dt_criacao}, "
            f"usuario_id={self.usuario_id})>"
        )