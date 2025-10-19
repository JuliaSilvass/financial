#controller/categoria_controller.py
import logging
from models.categoria import Categoria
from services.categoria_service import CategoriaServices
from services.session_manager import SessionManager

class CategoriaController:
    def __init__(self):
        self.service = CategoriaServices()

    def register_categoria(self, nome, usuario_id):
        """
        Cadastra uma nova categoria.
        """
        sucesso, mensagem = self.service.create_Categoria(
            nome=nome,
            usuario_id=usuario_id
        )

        if sucesso:
            logging.info(f"Categoria cadastrada com sucesso para usuário {usuario_id}.")
            return True, mensagem
        else:
            logging.error(f"Erro ao cadastrar categoria: {mensagem}")
            return False, mensagem
    
    def listar_categoria(self, usuario_id):
        sucesso, resultado = self.service.listar_categoria_por_usuario(usuario_id)
        if sucesso:
            return resultado  # Retorna a lista de categorias
        else:
            logging.error(resultado)
            return []

    def get_categoria(self, categoria_id):
        return self.service.get_categoria_by_id(categoria_id)

    def update_categoria(self, categoria_id, nome):
        return self.service.update_categoria(categoria_id, nome)

    def delete_categoria(self, categoria_id):
        return self.service.delete_categoria(categoria_id)
