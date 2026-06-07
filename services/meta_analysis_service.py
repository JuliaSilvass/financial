# services/meta_analysis_service.py

from datetime import date

class MetaAnalysisService:

    @staticmethod
    def calcular_progresso_valor(meta):
        if not meta.meta_valor_alvo or meta.meta_valor_alvo == 0:
            return 0

        progresso = float(meta.meta_valor_atual) / float(meta.meta_valor_alvo)

        return round(progresso * 100, 2)


    @staticmethod
    def calcular_progresso_tempo(meta):

        hoje = date.today()

        if not meta.meta_dt_inicial or not meta.meta_dt_limite:
            return 0

        dias_total = (meta.meta_dt_limite - meta.meta_dt_inicial).days

        if dias_total <= 0:
            return 0

        dias_passados = (hoje - meta.meta_dt_inicial).days

        progresso = dias_passados / dias_total

        return round(progresso * 100, 2)
    
    @staticmethod
    def calcular_viabilidade(
        meta,
        media_poupanca
    ):

        valor_necessario = (
            MetaAnalysisService
            .calcular_valor_mensal_necessario(meta)
        )

        if valor_necessario <= 0:
            return "Concluída"

        if media_poupanca >= valor_necessario:

            return "Viável"

        if media_poupanca >= valor_necessario * 0.7:

            return "Atenção"

        return "Pouco viável"

    @staticmethod
    def calcular_valor_mensal_necessario(meta):

        hoje = date.today()

        if not meta.meta_dt_limite:
            return 0

        valor_restante = (
            float(meta.meta_valor_alvo)
            - float(meta.meta_valor_atual)
        )

        if valor_restante <= 0:
            return 0

        meses_restantes = (
            (meta.meta_dt_limite.year - hoje.year) * 12
            + (meta.meta_dt_limite.month - hoje.month)
        )

        if meses_restantes <= 0:
            return valor_restante

        return round(
            valor_restante / meses_restantes,
            2
        )