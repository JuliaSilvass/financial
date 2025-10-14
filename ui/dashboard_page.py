import flet as ft
from services.session_manager import SessionManager

def dashboard_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/dashboard", controls=[])

    user = SessionManager.get_current_user()

    # Função de logout
    def logout_click(e):
        SessionManager.logout()
        page.go("/")

    # Função de navegação para cada área
    def navigate(area):
        page.snack_bar = ft.SnackBar(ft.Text(f"Navegando para: {area}"))
        page.snack_bar.open = True
        page.update()
        # Aqui futuramente você chamaria page.go("/area") para abrir a view correspondente

    # Menu lateral
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

    menu_buttons = [
        ft.ElevatedButton(text=item, on_click=lambda e, a=item: navigate(a), expand=True)
        for item in menu_items
    ]

    # Layout do dashboard
    return ft.View(
        route="/dashboard",
        controls=[
            ft.Row(
                controls=[
                    # Barra lateral
                    ft.Column(
                        controls=[
                            # ft.Text(f"Olá, {user.usuario_nome}", size=20, weight="bold"),
                            ft.Text(f"Olá", size=20, weight="bold"),
                            ft.Divider(height=2, thickness=1),
                            *menu_buttons,
                            ft.ElevatedButton("Logout", bgcolor="red", on_click=logout_click)
                        ],
                        width=200,
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    # Área principal
                    ft.Column(
                        controls=[
                            ft.Text("Bem-vindo ao Dashboard", size=30),
                            ft.Text("Use o menu à esquerda para navegar pelas funcionalidades do sistema."),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    )
                ],
                expand=True,
                spacing=20
            )
        ],
        padding=20,
        spacing=20
    )
