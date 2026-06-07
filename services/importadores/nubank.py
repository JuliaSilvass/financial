import csv
import re
from datetime import datetime
from datetime import date
import pdfplumber

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
        
        if arquivo.lower().endswith(".pdf"):

            return NubankImporter.importar_pdf(
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
    

    @staticmethod
    def importar_pdf(
        tipo_importacao,
        arquivo,
        conta_id,
        usuario_id,
        fatura_mes,
        fatura_ano
    ):

        try:

            db = SessionLocal()

            conta = (
                db.query(Conta)
                .filter(Conta.conta_id == conta_id)
                .first()
            )

            if not conta:
                return False, "Conta não encontrada."

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

            meses = {
                "JAN": 1,
                "FEV": 2,
                "MAR": 3,
                "ABR": 4,
                "MAI": 5,
                "JUN": 6,
                "JUL": 7,
                "AGO": 8,
                "SET": 9,
                "OUT": 10,
                "NOV": 11,
                "DEZ": 12
            }

            total_importadas = 0

            with pdfplumber.open(arquivo) as pdf:

                for page in pdf.pages:

                    texto = page.extract_text()

                    if not texto:
                        continue

                    linhas = texto.split("\n")

                    for linha in linhas:

                        linha = linha.strip()

                        if not linha:
                            continue

                        # ==========================================
                        # IGNORAR LIXO
                        # ==========================================

                        if "Pagamento em" in linha:
                            continue

                        if "Saldo restante" in linha:
                            continue

                        if "Total a pagar:" in linha:
                            continue

                        if "Conversão:" in linha:
                            continue

                        if linha.startswith("BRL "):
                            continue

                        if "TRANSAÇÕES DE" in linha:
                            continue

                        if "Pagamentos e Financiamentos" in linha:
                            continue

                        # Opcional: ignorar IOF
                        # if linha.startswith("20 MAI IOF"):
                        #     continue

                        # ==========================================
                        # REGEX PRINCIPAL
                        # ==========================================

                        match = re.match(
                            r"^(\d{2})\s+([A-Z]{3})\s+(.*?)\s+R\$\s+([\d\.,]+)$",
                            linha
                        )

                        if not match:
                            continue

                        dia = int(match.group(1))
                        mes_txt = match.group(2)
                        descricao = match.group(3).strip()

                        valor = float(
                            match.group(4)
                            .replace(".", "")
                            .replace(",", ".")
                        )

                        # ==========================================
                        # REMOVE MÁSCARA CARTÃO
                        # ==========================================

                        descricao = re.sub(
                            r"^••••\s+\d+\s+",
                            "",
                            descricao
                        )

                        descricao = descricao.strip()

                        # ==========================================
                        # DATA DA COMPRA
                        # ==========================================

                        mes_compra = meses[mes_txt]

                        ano_compra = int(fatura_ano)

                        if mes_compra > int(fatura_mes):
                            ano_compra -= 1

                        data_compra = date(
                            ano_compra,
                            mes_compra,
                            dia
                        )

                        # ==========================================
                        # PARCELAMENTO
                        # ==========================================

                        parcela_atual = 1
                        total_parcelas = 1

                        parcela = re.search(
                            r"(\d+)\/(\d+)",
                            descricao
                        )

                        if parcela:

                            parcela_atual = int(
                                parcela.group(1)
                            )

                            total_parcelas = int(
                                parcela.group(2)
                            )

                        # ==========================================
                        # LIMPA DESCRIÇÃO
                        # ==========================================

                        descricao_limpa = re.sub(
                            r"\s*-\s*Parcela\s*\d+\/\d+",
                            "",
                            descricao,
                            flags=re.IGNORECASE
                        )

                        descricao_limpa = descricao_limpa.strip()

                        # ==========================================
                        # CRIAR TRANSAÇÃO
                        # ==========================================

                        service = TransacaoService()

                        ok, msg = service.create_transacao(

                            descricao=descricao_limpa,

                            valor=abs(valor),

                            data=data_fatura,

                            ambiente_id='1',

                            categoria_id='1',

                            conta_id=conta_id,

                            tipo="despesa",

                            modo="credito",

                            pago=True,

                            local=None,

                            observacao="Importado automaticamente via PDF Nubank.",

                            recorrencia=False,

                            frequencia=None,

                            tipo_recorrencia=None,

                            dt_fim_recorrencia=None,

                            dt_pagamento=data_compra,

                            dt_vencimento=data_vencimento,

                            total_parcelas=int(total_parcelas),

                            parcela_atual=int(parcela_atual)
                        )

                        if ok:

                            total_importadas += 1

                        else:

                            print("ERRO:")
                            print(msg)

            return (
                True,
                f"{total_importadas} transações importadas via PDF."
            )

        except Exception as e:
            return False, str(e)