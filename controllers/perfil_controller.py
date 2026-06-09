from services.perfil_financeiro_service import (
    PerfilFinanceiroService
)


class PerfilController:

    def obter_perfil(
        self,
        usuario_id
    ):

        perfil = (
            PerfilFinanceiroService
            .calcular(usuario_id)
        )

        perfil["feedback"] = (
            PerfilFinanceiroService
            .gerar_feedback(perfil)
        )

        return perfil