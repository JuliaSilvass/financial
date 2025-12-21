import flet as ft
from services.session_manager import SessionManager
from utils.sidebar import build_sidebar

def dashboard_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/dashboard", controls=[])

    user = SessionManager.get_current_user()

    # -----------------------------
    # Menu
    # -----------------------------
    menu_items = [
        {"label": "Ambientes Financeiros", "route": "/ambiente/listar"},
        {"label": "Transações", "route": "/transacao/listar"},
        {"label": "Metas", "route": "/meta/listar"},
        {"label": "Categorias", "route": "/categoria/listar"},
        {"label": "Contas", "route": "/conta/listar"},
        {"label": "Relatórios", "route": "/relatorio"},
        {"label": "Compartilhamento", "route": "/compartilhamento"},
        {"label": "Perfil financeiro", "route": "/perfil"},
        {"label": "Configurações", "route": "/configuracao"},
    ]

    sidebar = build_sidebar(
                page=page,
                user=user,
                menu_items=menu_items,
                active_route="/dashboard"
            )

    # -----------------------------
    # VIEW
    # -----------------------------
    return ft.View(
        route="/dashboard",
        padding=20,
        bgcolor="#F5F5F5",
        controls=[
            ft.Row(
                expand=True,
                spacing=20,
                controls=[
                    # -----------------------------
                    # SIDEBAR
                    # -----------------------------
                    sidebar,

                    # -----------------------------
                    # ÁREA PRINCIPAL
                    # -----------------------------
                    ft.Container(
                        expand=True,
                        padding=ft.padding.all(30),
                        bgcolor="#FAFAFA",
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=8, color="#E0E0E0"),
                        content=ft.Column(
                            expand=True,
                            spacing=20,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Bem-vindo ao Dashboard",
                                    size=28,
                                    weight="bold",
                                    color="#1E3D59",
                                ),
                                ft.Text(
                                    "Use o menu à esquerda para navegar pelas funcionalidades do sistema.",
                                    size=16,
                                    color="#4F5B62",
                                ),
                            ],
                        ),
                    ),
                ],
            )
        ],
    )
