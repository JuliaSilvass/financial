#services/transacao_service.py
from sqlalchemy import extract

from models.transacao import Transacao
from models.ambiente import Ambiente
from sqlalchemy.orm import Session, joinedload
from database.connection_db import SessionLocal
from datetime import date
import logging

class TransacaoService:

    def __init__(self):
        self.db: Session = SessionLocal()
    
    # --------------------------------------------------------
    # Criação de nova transação
    # --------------------------------------------------------
    def create_transacao(self, descricao: str, valor: float, data: date, ambiente_id: int,
                                categoria_id: int, conta_id: int, tipo: str, modo: str, 
                                pago: bool = True,
                                # meta_id: int = None,
                                local: str = None,
                                observacao: str = None, recorrencia: bool = False, frequencia: str = None,
                                tipo_recorrencia: str = None, dt_fim_recorrencia: date = None, dt_pagamento: date = None,
                                dt_vencimento: date = None, total_parcelas: int = 1, parcela_atual: int = 1):
        try:
            nova_transacao = Transacao(
                descricao=descricao, valor=valor, data=data, ambiente_id=ambiente_id, 
                categoria_id=categoria_id, conta_id=conta_id, tipo=tipo, modo=modo, pago=pago, 
                # meta_id=meta_id,
                local=local, observacao=observacao, recorrencia=recorrencia, frequencia=frequencia,
                tipo_recorrencia=tipo_recorrencia, dt_fim_recorrencia=dt_fim_recorrencia, dt_pagamento=dt_pagamento,
                dt_vencimento=dt_vencimento, total_parcelas=total_parcelas, parcela_atual=parcela_atual
            )
            self.db.add(nova_transacao)
            self.db.commit()
            self.db.refresh(nova_transacao)
            logging.info(f"Transação '{descricao}' criada com sucesso (ID={nova_transacao.transacao_id})")
            return True, f"Transação '{descricao}' criada com sucesso!"
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao criar transação: {e}")
            return False, f"Erro ao criar transação: {str(e)}"
        finally:
            self.db.close()

    # --------------------------------------------------------
    # Listar transações por mês e ano
    # --------------------------------------------------------

    def listar_transacoes_por_mes(self, usuario_id: int, ano: int, mes: int):
        try:
            transacoes = (
                self.db.query(Transacao)
                .options(
                    joinedload(Transacao.ambiente),
                    joinedload(Transacao.categoria),
                    joinedload(Transacao.conta),
                )
                .join(Transacao.ambiente)
                .filter(
                    Ambiente.usuario_id == usuario_id,
                    extract("year", Transacao.transacao_data) == ano,
                    extract("month", Transacao.transacao_data) == mes,
                )
                .order_by(Transacao.transacao_data.desc())
                .all()
            )

            return True, transacoes

        except Exception as e:
            logging.error(f"Erro ao listar transações por mês: {e}")
            return False, str(e)

        finally:
            self.db.close()

    # --------------------------------------------------------
    # Listar todas as transações de todos os ambientes do usuário
    # --------------------------------------------------------
    def listar_transacoes_por_usuario(self, usuario_id: int):
        try:
            transacoes = (
                self.db.query(Transacao)
                .options(
                    joinedload(Transacao.ambiente),
                    joinedload(Transacao.categoria),
                    joinedload(Transacao.conta),
                )
                .join(Transacao.ambiente) 
                .filter(Ambiente.usuario_id == usuario_id)
                .order_by(Transacao.transacao_data.desc())
                .all()
            )

            return True, transacoes

        except Exception as e:
            logging.error(f"Erro ao listar transações do usuário {usuario_id}: {e}")
            return False, f"Erro ao listar transações: {e}"

        finally:
            self.db.close()

    # --------------------------------------------------------
    # Buscar transação por ID
    # --------------------------------------------------------
    def get_transacao_by_id(self, transacao_id: int):
        try:
            transacao = (
                self.db.query(Transacao)
                .filter(Transacao.transacao_id == transacao_id)
                .first()
            )
            return transacao
        except Exception as e:
            logging.error(f"Erro ao buscar transação: {e}")
            return None
        finally:
            self.db.close()

    # --------------------------------------------------------
    # Atualizar transação
    # --------------------------------------------------------
    def update_transacao(
        self,
        transacao_id: int,
        descricao: str,
        valor: float,
        data: date,
        ambiente_id: int,
        categoria_id: int,
        conta_id: int,
        tipo: str,
        modo: str,
        pago: bool,
        local: str = None,
        observacao: str = None,
        recorrencia: bool = False,
        frequencia: str = None,
        tipo_recorrencia: str = None,
        dt_fim_recorrencia: date = None,
        dt_pagamento: date = None,
        dt_vencimento: date = None,
        total_parcelas: int = 1,
        parcela_atual: int = 1,
    ):
        try:
            transacao = (
                self.db.query(Transacao)
                .filter(Transacao.transacao_id == transacao_id)
                .first()
            )
            if not transacao:
                return False, "Transação não encontrada."

            # Campos principais
            transacao.transacao_descricao = descricao
            transacao.transacao_valor = valor
            transacao.transacao_data = data
            transacao.transacao_ambiente_id = ambiente_id
            transacao.transacao_categoria_id = categoria_id
            transacao.conta_id = conta_id

            # Tipo / modo
            transacao.transacao_tipo = tipo
            transacao.transacao_modo = modo
            transacao.transacao_pago = pago

            # Extras
            transacao.transacao_local = local
            transacao.transacao_observacao = observacao
            transacao.transacao_recorrencia = recorrencia
            transacao.transacao_frequencia = frequencia
            transacao.transacao_tipo_recorrencia = tipo_recorrencia
            transacao.transacao_dt_fim_recorrencia = dt_fim_recorrencia
            transacao.transacao_dt_pagamento = dt_pagamento
            transacao.transacao_dt_vencimento = dt_vencimento
            transacao.transacao_total_parcelas = total_parcelas
            transacao.transacao_parcela_atual = parcela_atual

            self.db.commit()
            return True, "Transação atualizada com sucesso!"
        
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao atualizar transação: {e}")
            return False, f"Erro ao atualizar transação: {e}"
        
        finally:
            self.db.close()

    # --------------------------------------------------------
    # Excluir transação
    # --------------------------------------------------------
    def delete_transacao(self, transacao_id: int):
        try:
            transacao = (
                self.db.query(Transacao)
                .filter(Transacao.transacao_id == transacao_id)
                .first()
            )
            if not transacao:
                return False, "Transação não encontrada."

            self.db.delete(transacao)
            self.db.commit()
            return True, "Transação excluída com sucesso."
        
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao excluir transação: {e}")
            return False, f"Erro ao excluir transação: {e}"
        
        finally:
            self.db.close()