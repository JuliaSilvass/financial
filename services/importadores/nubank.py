import csv
import re
from datetime import datetime
from datetime import date

from services.transacao_service import TransacaoService
from models.ambiente import Ambiente
from models.categoria import Categoria
from models.conta import Conta
from database.connection_db import SessionLocal



class NubankImporter:

    @staticmethod
    def importar(
        tipo_importacao,
        arquivo,
        conta_id,
        usuario_id,
        fatura_mes,
        fatura_ano
    ):

        if arquivo.lower().endswith(".csv"):

            return NubankImporter.importar_csv(
                tipo_importacao,
                arquivo,
                conta_id,
                usuario_id,
                fatura_mes,
                fatura_ano
            )

        return False, "Formato não suportado."

    # ==========================================================
    # IMPORTAÇÃO CSV
    # ==========================================================

    @staticmethod
    def importar_csv(
        tipo_importacao,
        arquivo,
        conta_id,
        usuario_id,
        fatura_mes,
        fatura_ano
    ):

        try:

            service = TransacaoService()

            total_importadas = 0

            db = SessionLocal()

            ambiente = (
                db.query(Ambiente)
                .filter(Ambiente.usuario_id == usuario_id)
                .first()
            )

            categoria = (
                db.query(Categoria)
                .filter(Categoria.usuario_id == usuario_id)
                .first()
            )

            conta = (
                db.query(Conta)
                .filter(Conta.conta_id == conta_id)
                .first()
            )

            if not conta:
                return False, "Conta não encontrada."

            if not ambiente:
                return False, "Usuário não possui ambiente cadastrado."

            if not categoria:
                return False, "Usuário não possui categoria cadastrada."

            
            data_fatura = date(
                int(fatura_ano),
                int(fatura_mes),
                1
            )

            dia_vencimento = conta.conta_dia_vencimento or 1

            data_vencimento = date(
                int(fatura_ano),
                int(fatura_mes),
                int(dia_vencimento)
            )

            with open(
                arquivo,
                mode="r",
                encoding="utf-8"
            ) as csvfile:

                reader = csv.DictReader(csvfile)

                for row in reader:

                    # ==========================================
                    # CAMPOS CSV
                    # ==========================================

                    data = row["date"]
                    descricao = row["title"]
                    valor = float(row["amount"])

                    # ==========================================
                    # IGNORAR PAGAMENTO RECEBIDO
                    # ==========================================

                    if "pagamento recebido" in descricao.lower():
                        continue

                    # ==========================================
                    # DATA
                    # ==========================================

                    data_obj = datetime.strptime(
                        data,
                        "%Y-%m-%d"
                    ).date()

                    # ==========================================
                    # PARCELAMENTO
                    # ==========================================

                    parcela_atual = 1
                    total_parcelas = 1

                    match_parcela = re.search(
                        r"(\d+)\/(\d+)",
                        descricao
                    )

                    if match_parcela:

                        parcela_atual = int(
                            match_parcela.group(1)
                        )

                        total_parcelas = int(
                            match_parcela.group(2)
                        )

                    # ==========================================
                    # LIMPAR DESCRIÇÃO
                    # ==========================================

                    descricao_limpa = re.sub(
                        r"\s*-\s*Parcela\s*\d+\/\d+",
                        "",
                        descricao,
                        flags=re.IGNORECASE
                    )

                    descricao_limpa = re.sub(
                        r"\s*-\s*\d+\/\d+",
                        "",
                        descricao_limpa,
                        flags=re.IGNORECASE
                    )

                    descricao_limpa = descricao_limpa.strip()

                    # ==========================================
                    # CRIAR TRANSAÇÃO
                    # ==========================================

                    ok, msg = service.create_transacao(

                        descricao=descricao_limpa,

                        valor=abs(valor),

                        data=data_fatura,

                        ambiente_id='1',

                        categoria_id='1',

                        conta_id=conta_id,

                        tipo="despesa",

                        modo="credito" if tipo_importacao == "fatura" else "debito",

                        pago=True,

                        local=None,

                        observacao="Importado automaticamente via CSV Nubank.",

                        recorrencia=False,

                        frequencia=None,

                        tipo_recorrencia=None,

                        dt_fim_recorrencia=None,

                        dt_pagamento=data_obj,

                        dt_vencimento=data_vencimento if tipo_importacao == "fatura" else None,

                        total_parcelas=int(total_parcelas),

                        parcela_atual=int(parcela_atual)
                    )

                    if ok:
                        total_importadas += 1

            return (
                True,
                f"{total_importadas} transações importadas com sucesso."
            )

        except Exception as e:
            return False, str(e)