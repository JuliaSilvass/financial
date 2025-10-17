import logging
from models.ambiente import Ambiente
from services.ambiente_service import AmbienteServices 
from services.session_manager import SessionManager

class AmbienteController:
    def __init__(self):
        self.service = AmbienteServices()

    def register_ambiente(self, nome, descricao, usuario_id):
        """
        Cadastra um novo ambiente financeiro.
        """
        sucesso, mensagem = self.service.create_ambiente(
            nome=nome,
            descricao=descricao,
            usuario_id=usuario_id
        )

        if sucesso:
            logging.info(f"Ambiente cadastrado com sucesso para usuário {usuario_id}.")
            return True, mensagem
        else:
            logging.error(f"Erro ao cadastrar ambiente: {mensagem}")
            return False, mensagem
    
    def listar_ambientes(self, usuario_id):
        sucesso, resultado = self.service.listar_ambientes_por_usuario(usuario_id)
        if sucesso:
            return resultado  # lista de objetos Ambiente
        else:
            logging.error(resultado)
            return []
