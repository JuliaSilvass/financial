import logging
from models.conta import Conta
from services.conta_service import ContaService 
from services.session_manager import SessionManager

class ContaController:
    def __init__(self):
        self.service = ContaService()

    def register_conta(self, nome, tipo, saldo_inicial, saldo_disponivel, conta_ativo, usuario_id):
        """
        Cadastra uma nova conta financeiro.
        """
        sucesso, mensagem = self.service.create_conta(
            nome=nome,
            tipo=tipo,
            saldo_inicial=saldo_inicial,
            saldo_disponivel=saldo_disponivel,
            conta_ativo=conta_ativo,
            usuario_id=usuario_id
        )

        if sucesso:
            logging.info(f"Conta cadastrada com sucesso para usuário {usuario_id}.")
            return True, mensagem
        else:
            logging.error(f"Erro ao cadastrar conta: {mensagem}")
            return False, mensagem
    
    def listar_conta(self, usuario_id):
        sucesso, resultado = self.service.listar_conta_por_usuario(usuario_id)
        if sucesso:
            return resultado  
        else:
            logging.error(resultado)
            return []

    def update_conta(self, conta_id, nome, tipo, saldo_inicial, saldo_disponivel, conta_ativo):
        """
        Atualiza uma conta existente.
        """
        return self.service.update_conta(conta_id, nome, tipo, saldo_inicial, saldo_disponivel, conta_ativo)


    def get_conta(self, conta_id):
        return self.service.get_conta_by_id(conta_id)

    def delete_conta(self, conta_id):
        return self.service.delete_conta(conta_id)

