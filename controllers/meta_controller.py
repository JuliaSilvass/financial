import logging
from services.meta_service import MetaService
from models.meta import Meta
from services.session_manager import SessionManager


class MetaController:
    def __init__(self):
        self.service = MetaService()

    def _normalize(self, data: dict):
        return {
            k: None if v in ("", None) else v
            for k, v in data.items()
        }


    # --------------------------------------------------------
    # Cadastrar nova meta
    # --------------------------------------------------------
    def register_meta(
        self,
        nome,
        descricao,
        valor_alvo,
        valor_atual,
        data_inicio,
        data_fim,
        status,
        ambiente_id,
        usuario_id,
        # categoria_id
    ):
        """
        Trata os dados vazios convertendo-os para None.
        """
        payload = {
            "nome": nome,
            "descricao": descricao,
            "valor_alvo": valor_alvo,
            "valor_atual": valor_atual,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "status": status,
            "ambiente_id": ambiente_id,
            "usuario_id": usuario_id,
            # "categoria_id": categoria_id
        }

        payload = self._normalize(payload)

        """
        Cadastra uma nova meta no sistema.
        """
        sucesso, mensagem = self.service.create_meta(**payload)

        if sucesso:
            logging.info(f"Meta cadastrada com sucesso para usuário {SessionManager.get_current_user().get('id')}.")
            return True, mensagem
        else:
            logging.error(f"Erro ao cadastrar meta: {mensagem}")
            return False, mensagem

    # --------------------------------------------------------
    # Listar todas as metas de todos os ambientes do usuário
    # --------------------------------------------------------
    def listar_metas(self, usuario_id):
        sucesso, resultado = self.service.listar_meta_por_usuario(usuario_id)
        if sucesso:
            return resultado
        else:
            logging.error(resultado)
            return []

    # --------------------------------------------------------
    # Buscar meta por ID
    # --------------------------------------------------------
    def get_meta(self, meta_id: int):
        return self.service.get_meta_by_id(meta_id)


    # --------------------------------------------------------
    # Atualizar meta existente
    # --------------------------------------------------------
    def update_meta(
        self,
        meta_id,
        nome,
        descricao,
        valor_alvo,
        valor_atual,
        data_inicio,
        data_fim,
        status,
        ambiente_id,
        # categoria_id
    ):
        
        """
        Trata os dados vazios convertendo-os para None.
        """
        payload = {
            "meta_id": meta_id,
            "nome": nome,
            "descricao": descricao,
            "valor_alvo": valor_alvo,
            "valor_atual": valor_atual,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "status": status,
            "ambiente_id": ambiente_id,
            # "categoria_id": categoria_id
        }

        payload = self._normalize(payload)

        """
        Atualiza uma meta existente.
        """
        sucesso, mensagem = self.service.update_meta(**payload)

        if sucesso:
            logging.info(f"Meta atualizada com sucesso para usuário {SessionManager.get_current_user().get('id')}.")
            return True, mensagem
        else:
            logging.error(f"Erro ao atualizar meta: {mensagem}")
            return False, mensagem

    # --------------------------------------------------------
    # Excluir meta
    # --------------------------------------------------------
    def delete_meta(self, meta_id):
        return self.service.delete_meta(meta_id)
