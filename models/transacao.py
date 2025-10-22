# models/transacao.py
from sqlalchemy import Column, Integer, String, Text, Numeric, Date, Boolean, ForeignKey, TIMESTAMP, func
from database.connection_db import Base
from sqlalchemy.orm import relationship

class Transacao(Base):
    __tablename__ = "transacao"

    transacao_id = Column(Integer, primary_key=True, index=True)
    transacao_descricao = Column(Text, nullable=True)
    transacao_valor = Column(Numeric(12, 2), nullable=False)
    transacao_data = Column(Date, nullable=False)

    # Relações
    transacao_ambiente_id = Column(Integer, ForeignKey("ambiente.ambiente_id", ondelete="CASCADE"), nullable=False)
    transacao_categoria_id = Column(Integer, ForeignKey("categoria.categoria_id", ondelete="CASCADE"), nullable=False)
    transacao_meta_id = Column(Integer, ForeignKey("meta.meta_id", ondelete="SET NULL"), nullable=True)
    conta_id = Column(Integer, ForeignKey("conta.conta_id", ondelete="CASCADE"), nullable=False)

    # Informações adicionais
    transacao_local = Column(String(255), nullable=True)
    transacao_observacao = Column(Text, nullable=True)

    # Recorrência
    transacao_recorrencia = Column(Boolean, default=False)
    transacao_frequencia = Column(String(50), nullable=True)  # diária, semanal, mensal, anual
    transacao_tipo_recorrencia = Column(String(50), nullable=True)  # fixa ou variável
    transacao_dt_fim_recorrencia = Column(Date, nullable=True)

    # Tipo e modo
    transacao_modo = Column(String(50), nullable=False)  # débito, crédito, pix, etc.
    transacao_tipo = Column(String(50), nullable=False)  # receita ou despesa

    # Pagamento
    transacao_pago = Column(Boolean, default=True)
    transacao_dt_pagamento = Column(TIMESTAMP, server_default=func.now())
    transacao_dt_vencimento = Column(Date, nullable=True)

    # Parcelas
    transacao_total_parcelas = Column(Integer, default=1)
    transacao_parcela_atual = Column(Integer, default=1)

    def __init__(
        self, descricao, valor, data, ambiente_id, categoria_id,
        conta_id, tipo, modo, pago=True, meta_id=None, local=None, observacao=None,
        recorrencia=False, frequencia=None, tipo_recorrencia=None, dt_fim_recorrencia=None,
        dt_pagamento=None, dt_vencimento=None, total_parcelas=1, parcela_atual=1,
    ):
        self.transacao_descricao = descricao
        self.transacao_valor = valor
        self.transacao_data = data
        self.transacao_ambiente_id = ambiente_id
        self.transacao_categoria_id = categoria_id
        self.transacao_meta_id = meta_id
        self.transacao_local = local
        self.transacao_observacao = observacao
        self.transacao_recorrencia = recorrencia
        self.transacao_frequencia = frequencia
        self.transacao_tipo_recorrencia = tipo_recorrencia
        self.transacao_dt_fim_recorrencia = dt_fim_recorrencia
        self.transacao_modo = modo
        self.transacao_tipo = tipo
        self.transacao_pago = pago
        self.transacao_dt_pagamento = dt_pagamento
        self.transacao_dt_vencimento = dt_vencimento
        self.transacao_total_parcelas = total_parcelas
        self.transacao_parcela_atual = parcela_atual
        self.conta_id = conta_id

    def __repr__(self):
        return (
            f"<Transacao(id={self.transacao_id}, valor={self.transacao_valor}, tipo='{self.transacao_tipo}', "
            f"data={self.transacao_data}, conta_id={self.conta_id}), ambiente_id={self.transacao_ambiente_id}>"
        )

    ambiente = relationship("Ambiente", backref="transacoes")