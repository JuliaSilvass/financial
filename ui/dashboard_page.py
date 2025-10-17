import flet as ft
from services.session_manager import SessionManager

def dashboard_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/dashboard", controls=[])

    user = SessionManager.get_current_user()

    # --- Função de logout ---
    def logout_click(e):
        SessionManager.logout()
        page.go("/")

    # --- Função de navegação ---
    def navigate(area):
        if area == "Ambientes Financeiros":
            page.go("/ambiente/listar")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Navegando para: {area}"))
            page.snack_bar.open = True
            page.update()

    # --- Itens do menu lateral ---
    menu_items = [
        "Ambientes Financeiros",
        "Receitas e Despesas",
        "Metas",
        "Categorias",
        "Relatórios",
        "Compartilhamento",
        "Perfil Financeiro",
        "Configurações"
    ]

    # --- Botões do menu lateral ---
    menu_buttons = [
        ft.ElevatedButton(
            text=item,
            on_click=lambda e, a=item: navigate(a),
            expand=True,
            style=ft.ButtonStyle(
                bgcolor={"": "#44CFA1", "hovered": "#3AB08F"},
                color={"": "white"},
                padding=ft.padding.symmetric(vertical=12, horizontal=10),
                shape=ft.RoundedRectangleBorder(radius=8),
                overlay_color="#38A08B"
            )
        )
        for item in menu_items
    ]

    # --- Layout principal ---
    return ft.View(
        route="/dashboard",
        controls=[
            ft.Row(
                controls=[
                    # --- BARRA LATERAL ---
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Text(
                                        f"Olá, {user['nome']}",
                                        size=20,
                                        weight="bold",
                                        color="#1E3D59"
                                    ),
                                    padding=ft.padding.only(bottom=10)
                                ),
                                ft.Divider(height=2, thickness=1, color="#44CFA1"),
                                *menu_buttons,
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        "Logout",
                                        bgcolor="#F28B82",
                                        color="white",
                                        on_click=logout_click,
                                        style=ft.ButtonStyle(
                                            padding=ft.padding.symmetric(vertical=12),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            overlay_color="#E57373"
                                        )
                                    ),
                                    padding=ft.padding.only(top=20),
                                    width=190 
                                )
                            ],
                            spacing=12,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        width=230,
                        padding=ft.padding.all(15),
                        bgcolor="#E0F7FA",
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=8, color="#C8E6C9")
                    ),

                    # --- ÁREA PRINCIPAL ---
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Bem-vindo ao Dashboard 👋", size=28, weight="bold", color="#1E3D59"),
                                ft.Text(
                                    "Use o menu à esquerda para navegar pelas funcionalidades do sistema.",
                                    size=16,
                                    color="#4F5B62"
                                ),
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        ),
                        expand=True,
                        padding=ft.padding.all(30),
                        bgcolor="#FAFAFA",
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=8, color="#E0E0E0")
                    )
                ],
                expand=True,
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            )
        ],
        padding=20,
        bgcolor="#F5F5F5"
    )
