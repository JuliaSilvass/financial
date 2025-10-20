# models/conta.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey, func
from database.connection_db import Base

class Conta(Base):
    __tablename__ = "conta"

    conta_id = Column(Integer, primary_key=True, index=True)
    conta_nome = Column(String(200), nullable=False)
    conta_tipo = Column(String(50), nullable=False)
    conta_saldo_limite_inicial = Column(Numeric(12, 2), default=0)
    conta_saldo_limite_disponivel = Column(Numeric(12, 2), default=0)
    conta_ativo = Column(Boolean, default=True)
    conta_dt_criacao = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuario.usuario_id", ondelete="CASCADE"), nullable=False)

    def __init__(self, nome, tipo, saldo_inicial=0, saldo_disponivel=0, ativo=True, usuario_id=None):
        self.conta_nome = nome
        self.conta_tipo = tipo
        self.conta_saldo_limite_inicial = saldo_inicial
        self.conta_saldo_limite_disponivel = saldo_disponivel
        self.conta_ativo = ativo
        self.usuario_id = usuario_id

    def __repr__(self):
        return (
            f"<Conta(id={self.conta_id}, nome='{self.conta_nome}', tipo='{self.conta_tipo}', "
            f"ativo={self.conta_ativo}, usuario_id={self.usuario_id})>"
        )
