import flet as ft

from services.session_manager import SessionManager
from controllers.perfil_controller import PerfilController
from utils.sidebar import build_sidebar


# ==========================================================
# SIDEBAR
# ==========================================================

def perfil_sidebar(page, user, active_route: str):

    menu_items = [
        {
            "label": "Meu Perfil Financeiro",
            "route": "/perfil",
            "icon": ft.Icons.PERSON
        }
    ]

    return build_sidebar(
        page=page,
        user=user,
        menu_items=menu_items,
        active_route=active_route
    )


# ==========================================================
# PERFIL FINANCEIRO
# ==========================================================

def perfil_page(page: ft.Page):

    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/perfil", controls=[])

    user = SessionManager.get_current_user()

    controller = PerfilController()

    perfil = controller.obter_perfil(
        user["id"]
    )

    sidebar = perfil_sidebar(
        page,
        user,
        "/perfil"
    )

    def voltar_click(e):
        page.go("/dashboard")

    return ft.View(
        route="/perfil",
        padding=20,
        bgcolor="#F5F5F5",

        controls=[
            ft.Row(
                expand=True,
                spacing=20,

                controls=[

                    sidebar,

                    ft.Container(
                        expand=True,
                        padding=ft.padding.all(40),

                        bgcolor="#FAFAFA",

                        border_radius=10,

                        shadow=ft.BoxShadow(
                            blur_radius=8,
                            color="#E0E0E0"
                        ),

                        content=ft.Column(
                            spacing=20,

                            controls=[

                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            tooltip="Voltar",
                                            on_click=voltar_click
                                        ),

                                        ft.Text(
                                            "Perfil Financeiro",
                                            size=26,
                                            weight="bold"
                                        )
                                    ]
                                ),

                                ft.Divider(),

                                ft.Card(
                                    content=ft.Container(
                                        padding=20,

                                        content=ft.Column(
                                            spacing=15,

                                            controls=[

                                                ft.Text(
                                                    perfil["perfil"],
                                                    size=32,
                                                    weight="bold"
                                                ),

                                                ft.Text(
                                                    perfil["descricao"],
                                                    size=16
                                                ),

                                                ft.Divider(),

                                                ft.Text(
                                                    f"Receitas: R$ {perfil['receitas']:.2f}"
                                                ),

                                                ft.Text(
                                                    f"Despesas: R$ {perfil['despesas']:.2f}"
                                                ),

                                                ft.Text(
                                                    f"Percentual de Gastos: {perfil['percentual_gasto']}%"
                                                ),

                                                ft.Text(
                                                    f"Percentual de Poupança: {perfil['percentual_poupanca']}%"
                                                ),
                                            ]
                                        )
                                    )
                                ),
                            
                                ft.Card(
                                    content=ft.Container(
                                        padding=20,
                                        content=ft.Column(
                                            controls=[
                                                ft.Text(
                                                    "Análise Financeira",
                                                    size=20,
                                                    weight="bold"
                                                ),

                                                *[
                                                    ft.Text(
                                                        f"• {mensagem}"
                                                    )
                                                    for mensagem in perfil["feedback"]
                                                ]
                                            ]
                                        )
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        ]
    )