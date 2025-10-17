import flet as ft
from services.session_manager import SessionManager
from controllers.user_controller import UserController

def ambiente_cadastrar_page(page: ft.Page):
    # Verifica se há usuário logado
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/ambiente/cadastrar", controls=[])

    user = SessionManager.get_current_user()
    controller = UserController()

    # Funções auxiliares
    def logout_click(e):
        SessionManager.logout()
        page.go("/")

    def navigate(area):
        page.snack_bar = ft.SnackBar(ft.Text(f"Navegando para: {area}"))
        page.snack_bar.open = True
        page.update()

    # Campos do formulário
    nome_field = ft.TextField(label="Nome do Ambiente", width=400)
    desc_field = ft.TextField(label="Descrição", multiline=True, width=400)
    mensagem = ft.Text(color="green")

    def salvar_click(e):
        nome = nome_field.value.strip()
        descricao = desc_field.value.strip()

        if not nome:
            mensagem.value = "⚠️ O nome do ambiente é obrigatório."
            mensagem.color = "red"
        else:
            ok, msg = controller.register_ambiente(nome, descricao, user["id"])
            mensagem.value = msg
            mensagem.color = "green" if ok else "red"

            if ok:
                nome_field.value = ""
                desc_field.value = ""

        page.update()

    # Itens do menu lateral
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

    # Layout final da tela
    return ft.View(
        route="/ambiente/cadastrar",
        controls=[
            ft.Row(
                controls=[
                    # --- MENU LATERAL ---
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
                                ft.Text("Cadastrar Novo Ambiente ", size=28, weight="bold", color="#1E3D59"),
                                nome_field,
                                desc_field,
                                ft.ElevatedButton(
                                    text="Salvar Ambiente",
                                    icon=ft.Icons.SAVE,
                                    bgcolor="#44CFA1",
                                    color="white",
                                    on_click=salvar_click,
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(vertical=14, horizontal=25),
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        overlay_color="#3AB08F"
                                    )
                                ),
                                mensagem
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True,
                        padding=ft.padding.all(40),
                        bgcolor="#FAFAFA",
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=8, color="#E0E0E0")
                    )
                ],
                expand=True,
                spacing=20,
                alignment=ft.MainAxisAlignment.START
            )
        ],
        padding=20,
        bgcolor="#F5F5F5"
    )
