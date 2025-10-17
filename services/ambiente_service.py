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


    # Aqui o método para listar ambientes
    # def lista_ambientes_por_usuario(self, usuario_id: int):
    #     db: Session = SessionLocal()
    #     try:
    #         # Tratar
    #     except Exception as e:
    #         # Tratar
    #     finally:
    #         db.close()
    #         logging.info("Conexão com o banco de dados encerrada.")