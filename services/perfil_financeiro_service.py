from sqlalchemy import func

from database.connection_db import SessionLocal
from models.transacao import Transacao
from models.conta import Conta


class PerfilFinanceiroService:

    @staticmethod
    def calcular(usuario_id):

        db = SessionLocal()

        try:

            receitas = (
                db.query(
                    func.coalesce(
                        func.sum(
                            Transacao.transacao_valor
                        ),
                        0
                    )
                )
                .join(
                    Conta,
                    Conta.conta_id == Transacao.conta_id
                )
                .filter(
                    Conta.usuario_id == usuario_id,
                    Transacao.transacao_tipo == "receita"
                )
                .scalar()
            )

            despesas = (
                db.query(
                    func.coalesce(
                        func.sum(
                            Transacao.transacao_valor
                        ),
                        0
                    )
                )
                .join(
                    Conta,
                    Conta.conta_id == Transacao.conta_id
                )
                .filter(
                    Conta.usuario_id == usuario_id,
                    Transacao.transacao_tipo == "despesa"
                )
                .scalar()
            )

            quantidade_transacoes = (
                db.query(Transacao)
                .join(
                    Conta,
                    Conta.conta_id == Transacao.conta_id
                )
                .filter(
                    Conta.usuario_id == usuario_id
                )
                .count()
            )

            receitas = float(receitas or 0)
            despesas = float(despesas or 0)

            print("=" * 60)
            print("ANÁLISE PERFIL FINANCEIRO")
            print(f"USUÁRIO: {usuario_id}")
            print(f"RECEITAS: {receitas}")
            print(f"DESPESAS: {despesas}")
            print(f"TRANSAÇÕES: {quantidade_transacoes}")
            print("=" * 60)

            # ----------------------------------------------------
            # DESLIGADO
            # ----------------------------------------------------

            if quantidade_transacoes < 5:

                return {
                    "perfil": "Desligado",
                    "descricao": (
                        "Pouco envolvimento com o "
                        "controle financeiro."
                    ),
                    "receitas": receitas,
                    "despesas": despesas,
                    "percentual_gasto": 0,
                    "percentual_poupanca": 0
                }

            # ----------------------------------------------------
            # SEM RECEITAS
            # ----------------------------------------------------

            if receitas <= 0:

                return {
                    "perfil": "Descontrolado",
                    "descricao": (
                        "Não há receitas registradas "
                        "para análise financeira."
                    ),
                    "receitas": receitas,
                    "despesas": despesas,
                    "percentual_gasto": 0,
                    "percentual_poupanca": 0
                }

            percentual_gasto = (
                despesas / receitas
            ) * 100

            percentual_poupanca = (
                100 - percentual_gasto
            )

            print(f"% GASTO: {percentual_gasto:.2f}")
            print(f"% POUPANÇA: {percentual_poupanca:.2f}")

            # ----------------------------------------------------
            # DESCONTROLADO
            # ----------------------------------------------------

            if despesas > receitas:

                perfil = "Descontrolado"

                descricao = (
                    "As despesas estão acima "
                    "das receitas."
                )

            # ----------------------------------------------------
            # FINANCISTA
            # ----------------------------------------------------

            elif percentual_poupanca >= 30:

                perfil = "Financista"

                descricao = (
                    "Apresenta forte capacidade "
                    "de poupança e planejamento."
                )

            # ----------------------------------------------------
            # POUPADOR
            # ----------------------------------------------------

            elif percentual_poupanca >= 20:

                perfil = "Poupador"

                descricao = (
                    "Possui hábito consistente "
                    "de poupança."
                )

            # ----------------------------------------------------
            # GASTADOR
            # ----------------------------------------------------

            else:

                perfil = "Gastador"

                descricao = (
                    "Grande parte da renda é "
                    "destinada ao consumo."
                )

            return {
                "perfil": perfil,
                "descricao": descricao,
                "receitas": receitas,
                "despesas": despesas,
                "percentual_gasto": round(
                    percentual_gasto,
                    2
                ),
                "percentual_poupanca": round(
                    percentual_poupanca,
                    2
                )
            }

        finally:
            db.close()

    @staticmethod
    def gerar_feedback(perfil_data):

        perfil = perfil_data["perfil"]

        if perfil == "Desligado":

            return [
                "Poucas movimentações foram registradas.",
                "Registre receitas e despesas regularmente.",
                "Acompanhar suas finanças permite análises mais precisas."
            ]

        if perfil == "Descontrolado":

            return [
                "Não há receitas suficientes para análise.",
                "Cadastre suas fontes de renda.",
                "Monitore seus gastos para melhorar o planejamento financeiro."
            ]

        if perfil == "Gastador":

            return [
                "Grande parte da renda está comprometida com despesas.",
                "Avalie gastos não essenciais.",
                "Considere criar uma reserva financeira."
            ]

        if perfil == "Poupador":

            return [
                "Você apresenta bons hábitos financeiros.",
                "Mantenha sua capacidade de poupança.",
                "Considere transformar parte da reserva em investimentos."
            ]

        if perfil == "Financista":

            return [
                "Você demonstra elevado nível de planejamento financeiro.",
                "Continue acompanhando seus objetivos.",
                "Avalie estratégias de diversificação patrimonial."
            ]

        return [
            "Não foi possível gerar recomendações."
        ]