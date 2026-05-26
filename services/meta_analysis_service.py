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