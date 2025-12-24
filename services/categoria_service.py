#services/categoria_service.py
from models.categoria import Categoria
from sqlalchemy.orm import Session
from database.connection_db import SessionLocal
import logging

class CategoriaServices:

    def __init__(self):
        self.db: Session = SessionLocal()
    
    # Aqui o método para criar ambiente
    def create_Categoria(self, nome: str, usuario_id: int):
        try:
            categoria_existente = (
                self.db.query(Categoria)
                .filter(
                    Categoria.usuario_id == usuario_id,
                    Categoria.categoria_nome.ilike(nome)
                )
                .first()
            )

            if categoria_existente:
                return False, "Já existe uma categoria com esse nome."

            novo_categoria = Categoria(
                nome=nome,
                usuario_id=usuario_id
            )
            self.db.add(novo_categoria)
            self.db.commit()
            self.db.refresh(novo_categoria)
            logging.info(f"Categoria '{nome}' criada com sucesso (ID={novo_categoria.categoria_id})")
            return True, f"Categoria '{nome}' criada com sucesso!"
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao criar categoria: {e}")
            return False, f"Erro ao criar categoria: {str(e)}"
        finally:
            self.db.close()


    # Aqui o método para categoria por usuário
    def listar_categoria_por_usuario(self, usuario_id: int):
        try:
            ambientes = (
                self.db.query(Categoria)
                .filter(Categoria.usuario_id == usuario_id)
                .order_by(Categoria.categoria_id.desc())
                .all()
            )
            return True, ambientes
        except Exception as e:
            logging.error(f"Erro ao listar categorias: {e}")
            return False, f"Erro ao listar categorias: {e}"
        finally:
            self.db.close()

    # seleciona categoria por id
    def get_categoria_by_id(self, categoria_id: int):
        try:
            categoria = self.db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
            return categoria
        except Exception as e:
            logging.error(f"Erro ao buscar categoria: {e}")
            return None
        finally:
            self.db.close()

    # altera categoria 
    def update_categoria(self, categoria_id: int, nome: str, usuario_id: int):
        try:
            categoria_existente = (
                self.db.query(Categoria)
                .filter(
                    Categoria.usuario_id == usuario_id,
                    Categoria.categoria_nome.ilike(nome)
                )
                .first()
            )

            if categoria_existente:
                return False, "Já existe uma categoria com esse nome."

            categoria = self.db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
            if not categoria:
                return False, "categoria não encontrada."

            categoria.categoria_nome = nome
            self.db.commit()
            return True, "Categoria atualizada com sucesso!"
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao atualizar categoria: {e}")
            return False, f"Erro: {e}"
        finally:
            self.db.close()

    # exclui ambiente
    def delete_categoria(self, categoria_id: int):
        try:
            categoria = self.db.query(Categoria).filter(Categoria.categoria_id == categoria_id).first()
            if not categoria:
                return False, "Categoria não encontrada."
            self.db.delete(categoria)
            self.db.commit()
            return True, "Categoria excluída com sucesso."
        except Exception as e:
            self.db.rollback()
            logging.error(f"Erro ao excluir categoria: {e}")
            return False, f"Erro ao excluir categoria: {e}"
        finally:
            self.db.close()
