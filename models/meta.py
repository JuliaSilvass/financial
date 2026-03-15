# models/meta.py
from sqlalchemy import Column, Integer, String, Text, Numeric, Date, Boolean, ForeignKey, TIMESTAMP, func
from database.connection_db import Base
from sqlalchemy.orm import relationship
from models.ambiente import Ambiente
from models.categoria import Categoria
from models.conta import Conta
from models.transacao import Transacao

class Meta(Base):
    __tablename__ = "meta"

    meta_id = Column(Integer, primary_key=True, index=True)
    meta_nome = Column(String(255), nullable=False)
    meta_descricao = Column(Text, nullable=True)
    meta_valor_alvo = Column(Numeric(12, 2), nullable=False)
    meta_valor_atual = Column(Numeric(12, 2), default=0)
    meta_dt_inicial = Column(Date, nullable=False)
    meta_dt_limite = Column(Date, nullable=True)
    meta_concluida = Column(Boolean, default=False)
    usuario_id = Column(Integer, ForeignKey("usuario.usuario_id"), nullable=False)

    # Relações
    ambiente_id = Column(Integer, ForeignKey("ambiente.ambiente_id", ondelete="CASCADE"), nullable=False)
    # categoria_id = Column(Integer, ForeignKey("categoria.categoria_id", ondelete="CASCADE"), nullable=False)

    ambiente = relationship("Ambiente", backref="metas")
    # categoria = relationship("Categoria", backref="metas")

    def __init__(
        self, nome, descricao, 
        valor_alvo, valor_atual, data_inicio, 
        data_fim, status, ambiente_id, usuario_id
    ):
        self.meta_nome = nome
        self.meta_descricao = descricao
        self.meta_valor_alvo = valor_alvo
        self.meta_valor_atual = valor_atual
        self.meta_dt_inicial = data_inicio
        self.meta_dt_limite = data_fim
        self.meta_concluida = status
        self.ambiente_id = ambiente_id
        self.usuario_id = usuario_id
        # self.meta_categoria_id = categoria_id

    def __repr__(self):
        return (
            f"<Meta(id={self.meta_id}, nome='{self.meta_nome}', valor_alvo={self.meta_valor_alvo}, "
            f"dt_inicial={self.meta_dt_inicial}, dt_limite={self.meta_dt_limite}, ambiente_id={self.ambiente_id})>"
        )
    