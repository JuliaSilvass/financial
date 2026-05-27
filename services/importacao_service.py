# services/importacao_service.py

from services.importadores.nubank import NubankImporter


class ImportacaoService:

    @staticmethod
    def importar(
        banco,
        tipo_importacao,
        arquivo,
        conta_id,
        usuario_id,
        fatura_mes=None,
        fatura_ano=None
    ):

        # ======================================================
        # NUBANK
        # ======================================================

        if banco == "nubank":

            return NubankImporter.importar(
                tipo_importacao=tipo_importacao,
                arquivo=arquivo,
                conta_id=conta_id,
                usuario_id=usuario_id,
                fatura_mes=fatura_mes,
                fatura_ano=fatura_ano
            )

        # ======================================================
        # BANCO NÃO IMPLEMENTADO
        # ======================================================

        return False, "Banco ainda não implementado."