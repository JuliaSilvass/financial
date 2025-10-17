#services/ambiente_service.py
from models.ambiente import Ambiente
from sqlalchemy.orm import Session
from database.connection_db import SessionLocal
import logging

class AmbienteServices:

    def __init__(self):
        self.db: Session = SessionLocal()
    
    # Aqui o método para criar ambiente
    def create_ambiente(self, nome: str, descricao: str, usuario_id: int):
        try:
            novo_ambiente = Ambiente(
                nome=nome,
                descricao=descricao,
                usuario_id=usuario_id
            )
            self.db.add(novo_ambiente)
            self.db.commit()
            self.db.refresh(novo_ambiente)
            logging.info(f"Ambiente '{nome}' criado com sucesso (ID={novo_ambiente.ambiente_id})")
            return True, f"Ambiente '{nome}' criado com sucesso!"
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao criar ambiente: {e}")
            return False, f"Erro ao criar ambiente: {str(e)}"
        finally:
            self.db.close()


    # Aqui o método para listar ambientes por usuário
    def listar_ambientes_por_usuario(self, usuario_id: int):
        try:
            ambientes = (
                self.db.query(Ambiente)
                .filter(Ambiente.usuario_id == usuario_id)
                .order_by(Ambiente.ambiente_dt_criacao.desc())
                .all()
            )
            return True, ambientes
        except Exception as e:
            logging.error(f"Erro ao listar ambientes: {e}")
            return False, f"Erro ao listar ambientes: {e}"
        finally:
            self.db.close()

    # seleciona ambiente por id
    def get_ambiente_by_id(self, ambiente_id: int):
        try:
            ambiente = self.db.query(Ambiente).filter(Ambiente.ambiente_id == ambiente_id).first()
            return ambiente
        except Exception as e:
            logging.error(f"Erro ao buscar ambiente: {e}")
            return None
        finally:
            self.db.close()

    # altera ambiente 
    def update_ambiente(self, ambiente_id: int, nome: str, descricao: str):
        try:
            ambiente = self.db.query(Ambiente).filter(Ambiente.ambiente_id == ambiente_id).first()
            if not ambiente:
                return False, "Ambiente não encontrado."

            ambiente.ambiente_nome = nome
            ambiente.ambiente_descricao = descricao
            self.db.commit()
            return True, "Ambiente atualizado com sucesso!"
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao atualizar ambiente: {e}")
            return False, f"Erro: {e}"
        finally:
            self.db.close()

    # exclui ambiente
    def delete_ambiente(self, ambiente_id: int):
        try:
            ambiente = self.db.query(Ambiente).filter(Ambiente.ambiente_id == ambiente_id).first()
            if not ambiente:
                return False, "Ambiente não encontrado."
            self.db.delete(ambiente)
            self.db.commit()
            return True, "Ambiente excluído com sucesso."
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao excluir ambiente: {e}")
            return False, f"Erro ao excluir ambiente: {e}"
        finally:
            self.db.close()

