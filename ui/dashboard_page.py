import flet as ft
from services.session_manager import SessionManager

def dashboard_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/dashboard", controls=[])

    user = SessionManager.get_current_user()

    # -----------------------------
    # Ações
    # -----------------------------
    def logout_click(e):
        SessionManager.logout()
        page.go("/")

    def navigate(area):
        if area == "Ambientes Financeiros":
            page.go("/ambiente/listar")
        elif area == "Categorias":
            page.go("/categoria/listar")
        elif area == "Contas":
            page.go("/conta/listar")
        elif area == "Transações":
            page.go("/transacao/listar")
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Navegando para: {area}"))
            page.snack_bar.open = True
            page.update()

    # -----------------------------
    # Menu
    # -----------------------------
    menu_items = [
        "Ambientes Financeiros",
        "Transações",
        "Metas",
        "Categorias",
        "Contas",
        "Relatórios",
        "Compartilhamento",
        "Perfil Financeiro",
        "Configurações"
    ]

    menu_buttons = [
        ft.Container(
            width=float("inf"),
            content=ft.ElevatedButton(
                text=item,
                on_click=lambda e, a=item: navigate(a),
                style=ft.ButtonStyle(
                    bgcolor={"": "#44CFA1", "hovered": "#3AB08F"},
                    color={"": "white"},
                    padding=ft.padding.symmetric(vertical=14),
                    shape=ft.RoundedRectangleBorder(radius=8),
                    overlay_color="#38A08B",
                ),
            ),
        )
        for item in menu_items
    ]

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
                    ft.Container(
                        width=230,
                        padding=ft.padding.all(15),
                        bgcolor="#E0F7FA",
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=8, color="#C8E6C9"),
                        content=ft.Column(
                            expand=True,  
                            spacing=12,
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            controls=[
                                ft.Text(
                                    f"Olá, {user['nome']}",
                                    size=20,
                                    weight="bold",
                                    color="#1E3D59",
                                ),

                                ft.Divider(height=2, thickness=1, color="#44CFA1"),

                                *menu_buttons,
                                
                                ft.Container(expand=True),

                                ft.ElevatedButton(
                                    "Logout",
                                    bgcolor="#F28B82",
                                    color="white",
                                    on_click=logout_click,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(vertical=12),
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        overlay_color="#E57373",
                                    ),
                                ),
                            ],
                        ),
                    ),

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
