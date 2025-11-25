import logging
from models.transacao import Transacao
from services.transacao_service import TransacaoService
from services.session_manager import SessionManager


class TransacaoController:
    def __init__(self):
        self.service = TransacaoService()

    # --------------------------------------------------------
    # Cadastrar nova transação
    # --------------------------------------------------------
    def register_transacao(
        self,
        descricao,
        valor,
        data,
        ambiente_id,
        categoria_id,
        conta_id,
        tipo,
        modo,
        pago=True,
        # meta_id=None,
        local=None,
        observacao=None,
        recorrencia=False,
        frequencia=None,
        tipo_recorrencia=None,
        dt_fim_recorrencia=None,
        dt_pagamento=None,
        dt_vencimento=None,
        total_parcelas=1,
        parcela_atual=1,
    ):
        """
        Cadastra uma nova transação no sistema.
        """
        sucesso, mensagem = self.service.create_transacao(
            descricao=descricao,
            valor=valor,
            data=data,
            ambiente_id=ambiente_id,
            categoria_id=categoria_id,
            conta_id=conta_id,
            tipo=tipo,
            modo=modo,
            pago=pago,
            # meta_id=meta_id,
            local=local,
            observacao=observacao,
            recorrencia=recorrencia,
            frequencia=frequencia,
            tipo_recorrencia=tipo_recorrencia,
            dt_fim_recorrencia=dt_fim_recorrencia,
            dt_pagamento=dt_pagamento,
            dt_vencimento=dt_vencimento,
            total_parcelas=total_parcelas,
            parcela_atual=parcela_atual,
        )

        if sucesso:
            logging.info(f"Transação cadastrada com sucesso para usuário {SessionManager.get_current_user().get('id')}.")
            return True, mensagem
        else:
            logging.error(f"Erro ao cadastrar transação: {mensagem}")
            return False, mensagem

    # --------------------------------------------------------
    # Listar todas as transações de todos os ambientes do usuário
    # --------------------------------------------------------
    def listar_transacoes(self, usuario_id):
        sucesso, resultado = self.service.listar_transacoes_por_usuario(usuario_id)
        if sucesso:
            return resultado
        else:
            logging.error(resultado)
            return []

    # --------------------------------------------------------
    # Buscar transação por ID
    # --------------------------------------------------------
    def get_transacao(self, transacao_id):
        return self.service.get_transacao_by_id(transacao_id)

    # --------------------------------------------------------
    # Atualizar transação existente
    # --------------------------------------------------------
    def update_transacao(
        self,
        transacao_id,
        descricao,
        valor,
        tipo,
        modo,
        pago,
        observacao=None,
        local=None,
        dt_vencimento=None
    ):
        """
        Atualiza uma transação existente.
        """
        return self.service.update_transacao(
            transacao_id,
            descricao,
            valor,
            tipo,
            modo,
            pago,
            observacao,
            local,
            dt_vencimento,
        )

    # --------------------------------------------------------
    # Excluir transação
    # --------------------------------------------------------
    def delete_transacao(self, transacao_id):
        return self.service.delete_transacao(transacao_id)
