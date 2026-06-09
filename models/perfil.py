from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    TIMESTAMP,
    ForeignKey,
    func
)

from database.connection_db import Base


class Perfil(Base):

    __tablename__ = "perfil"

    perfil_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer,ForeignKey("usuario.usuario_id", ondelete="CASCADE"), nullable=False)
    perfil_tipo = Column(String(50), nullable=False)
    perfil_descricao = Column(Text)
    perfil_percentual_gastos = Column(Numeric(5, 2))
    perfil_percentual_poupanca = Column(Numeric(5, 2))
    perfil_receita_total = Column(Numeric(12, 2))
    perfil_despesa_total = Column(Numeric(12, 2))
    perfil_dt_calculo = Column(TIMESTAMP,server_default=func.now())