#services/meta_service.py
from sqlalchemy import extract
from models.conta import Conta
from models.transacao import Transacao
from models.ambiente import Ambiente
from models.categoria import Categoria
from models.meta import Meta
from sqlalchemy.orm import Session, joinedload
from database.connection_db import SessionLocal
from datetime import date
from decimal import Decimal
import logging

class MetaService:

    def __init__(self):
        self.db: Session = SessionLocal()
    
    # --------------------------------------------------------
    # Criação de nova meta
    # --------------------------------------------------------
    def create_meta(self, nome: str, descricao: str, valor_alvo: Decimal, valor_atual: Decimal, 
                    data_inicio: date, data_fim: date, status: bool, ambiente_id: int, usuario_id: int):

        try:
            valor_alvo = Decimal(str(valor_alvo))
            valor_atual = Decimal(str(valor_atual))

            nova_meta = Meta(
                nome=nome,
                descricao=descricao,
                valor_alvo=valor_alvo,
                valor_atual=valor_atual,
                data_inicio=data_inicio,
                data_fim=data_fim,
                status=status,
                ambiente_id=ambiente_id,
                usuario_id=usuario_id
            )

            self.db.add(nova_meta)
            self.db.commit()
            self.db.refresh(nova_meta)

            logging.info(f"Meta '{nome}' criada com sucesso (ID={nova_meta.meta_id})")

            return True, f"Meta '{nome}' criada com sucesso!"

        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao criar meta: {e}")
            return False, f"Erro ao criar meta: {e}"

        finally:
            self.db.close()

    # --------------------------------------------------------
    # Listar todas as meta do usuário
    # --------------------------------------------------------
    def listar_meta_por_usuario(self, usuario_id: int):
        try:
            meta = (
                self.db.query(Meta)
                .join(Meta.ambiente)
                .filter(Ambiente.usuario_id == usuario_id)
                .order_by(Meta.meta_dt_limite.desc())
                .all()
            )
            return True, meta
        except Exception as e:
            logging.error(f"Erro ao listar meta do usuário {usuario_id}: {e}")
            return False, f"Erro ao listar meta: {e}"
        finally:
            self.db.close()



    # --------------------------------------------------------
    # Buscar meta por ID
    # --------------------------------------------------------
    def get_meta_by_id(self, meta_id: int):
        try:
            meta = (
                self.db.query(Meta)
                .filter(Meta.meta_id == meta_id)
                .first()
            )
            return meta
        except Exception as e:
            logging.error(f"Erro ao buscar meta: {e}")
            return None
        finally:
            self.db.close()

    # --------------------------------------------------------
    # Atualizar meta
    # --------------------------------------------------------
    def update_meta(
        self,
        meta_id: int,
        nome: str,
        descricao: str,
        valor_alvo: float,
        valor_atual: float,
        data_inicio: date,
        data_fim: date,
        status: bool,
        ambiente_id: int,
    ):
        try:
            meta = (
                self.db.query(Meta)
                .filter(Meta.meta_id == meta_id)
                .first()
            )
            if not meta:
                return False, "Meta não encontrada."

            # Campos principais
            meta.meta_nome = nome
            meta.meta_descricao = descricao
            meta.meta_valor_alvo = valor_alvo
            meta.meta_valor_atual = valor_atual
            meta.meta_dt_inicial = data_inicio
            meta.meta_dt_limite = data_fim
            meta.meta_concluida = status
            meta.ambiente_id = ambiente_id
            # meta.meta_categoria_id = categoria_id

            self.db.commit()
            return True, "Meta atualizada com sucesso!"
        
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao atualizar meta: {e}")
            return False, f"Erro ao atualizar meta: {e}"
        
        finally:
            self.db.close()

    # --------------------------------------------------------
    # Excluir meta
    # --------------------------------------------------------
    def delete_meta(self, meta_id: int):
        try:
            meta = (
                self.db.query(Meta)
                .filter(Meta.meta_id == meta_id)
                .first()
            )
            if not meta:
                return False, "Meta não encontrada."

            self.db.delete(meta)
            self.db.commit()
            return True, "Meta excluída com sucesso."
        
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao excluir meta: {e}")
            return False, f"Erro ao excluir meta: {e}"
        
        finally:
            self.db.close()