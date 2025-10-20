#services/conta_service.py
from models.conta import Conta
from sqlalchemy.orm import Session
from database.connection_db import SessionLocal
import logging

class ContaService:

    def __init__(self):
        self.db: Session = SessionLocal()
    
    # Aqui o método para criar conta
    def create_conta(self, nome: str, tipo: str, saldo_inicial:float, saldo_disponivel: float, conta_ativo:bool, usuario_id: int):
        try:
            nova_conta = Conta(
                nome=nome,
                tipo=tipo,
                saldo_inicial=saldo_inicial,
                saldo_disponivel=saldo_disponivel,
                ativo=conta_ativo,  
                usuario_id=usuario_id
            )
            self.db.add(nova_conta)
            self.db.commit()
            self.db.refresh(nova_conta)
            logging.info(f"Conta '{nome}' criada com sucesso (ID={nova_conta.conta_id})")
            return True, f"Conta '{nome}' criada com sucesso!"
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao criar conta: {e}")
            return False, f"Erro ao criar conta: {str(e)}"
        finally:
            self.db.close()


    # Aqui o método para listar conta por usuário
    def listar_conta_por_usuario(self, usuario_id: int):
        try:
            conta = (
                self.db.query(Conta)
                .filter(Conta.usuario_id == usuario_id)
                .order_by(Conta.conta_dt_criacao.desc())
                .all()
            )
            return True, conta
        except Exception as e:
            logging.error(f"Erro ao listar contas: {e}")
            return False, f"Erro ao listar contas: {e}"
        finally:
            self.db.close()

    # seleciona conta por id
    def get_conta_by_id(self, conta_id: int):
        try:
            conta = self.db.query(Conta).filter(Conta.conta_id == conta_id).first()
            return conta
        except Exception as e:
            logging.error(f"Erro ao buscar conta: {e}")
            return None
        finally:
            self.db.close()

    # altera conta  
    def update_conta(self, conta_id: int, nome: str, tipo: str, saldo_inicial: float, saldo_disponivel: float, conta_ativo:bool):
        try:
            conta = self.db.query(Conta).filter(Conta.conta_id == conta_id).first()
            if not conta:
                return False, "Conta não encontrada."

            conta.conta_nome = nome
            conta.conta_tipo = tipo
            conta.conta_saldo_limite_inicial = saldo_inicial
            conta.conta_saldo_limite_disponivel = saldo_disponivel
            conta.conta_ativo = conta_ativo
            self.db.commit()
            return True, "Conta atualizada com sucesso!"
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao atualizar conta: {e}")
            return False, f"Erro: {e}"
        finally:
            self.db.close()

    # exclui conta
    def delete_conta(self, conta_id: int):
        try:
            conta = self.db.query(Conta).filter(Conta.conta_id == conta_id).first()
            if not conta:
                return False, "Conta não encontrada."
            self.db.delete(conta)
            self.db.commit()
            return True, "Conta excluída com sucesso."
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao excluir conta: {e}")
            return False, f"Erro ao excluir conta: {e}"
        finally:
            self.db.close()

