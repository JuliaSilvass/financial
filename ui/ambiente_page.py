import flet as ft
from services.session_manager import SessionManager
from controllers.ambiente_controller import AmbienteController


# ----------------------------------------------------------
# 🔹 Função utilitária para criar a barra lateral unificada
# ----------------------------------------------------------
def barra_lateral(user, page, current_page):
    """Cria a barra lateral com os botões corretos ativos/desativados"""
    
    def go_to_listar(e):
        if current_page != "listar":
            page.go("/ambiente/listar")

    def go_to_cadastrar(e):
        if current_page != "cadastrar":
            page.go("/ambiente/cadastrar")

    def logout_click(e):
        SessionManager.logout()
        page.go("/")

    return ft.Container(
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

                # Botões principais da barra lateral
                ft.ElevatedButton(
                    text="Listar Ambientes",
                    icon=ft.Icons.LIST,
                    bgcolor="#44CFA1" if current_page == "listar" else "#B2DFDB",
                    color="white" if current_page == "listar" else "#1E3D59",
                    on_click=go_to_listar if current_page != "listar" else None,
                    disabled=current_page == "listar",
                    expand=True
                ),
                ft.ElevatedButton(
                    text="Cadastrar Novo",
                    icon=ft.Icons.ADD,
                    bgcolor="#44CFA1" if current_page == "cadastrar" else "#B2DFDB",
                    color="white" if current_page == "cadastrar" else "#1E3D59",
                    on_click=go_to_cadastrar if current_page != "cadastrar" else None,
                    disabled=current_page == "cadastrar",
                    expand=True
                ),
                ft.Divider(height=2, thickness=1, color="#44CFA1"),
                ft.ElevatedButton(
                    text="Logout",
                    bgcolor="#F28B82",
                    color="white",
                    on_click=logout_click,
                )
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=230,
        padding=ft.padding.all(15),
        bgcolor="#E0F7FA",
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=8, color="#C8E6C9")
    )


# --------------------------------------------------------------------
# 📋 Página de CADASTRO
# --------------------------------------------------------------------
def ambiente_cadastrar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/ambiente/cadastrar", controls=[])

    user = SessionManager.get_current_user()
    controller = AmbienteController()

    # Campos do formulário
    nome_field = ft.TextField(label="Nome do Ambiente", width=400)
    desc_field = ft.TextField(label="Descrição", multiline=True, width=400)
    mensagem = ft.Text(color="green")

    # Voltar
    def voltar_click(e):
        page.go("/ambiente/listar")

    # Salvar
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
                page.snack_bar = ft.SnackBar(ft.Text("✅ Ambiente cadastrado com sucesso!"))
                page.snack_bar.open = True
                page.update()
                page.go("/ambiente/listar")
                return
        page.update()

    # Layout principal
    return ft.View(
        route="/ambiente/cadastrar",
        controls=[
            ft.Row(
                controls=[
                    barra_lateral(user, page, "cadastrar"),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            tooltip="Voltar para listagem",
                                            on_click=voltar_click
                                        ),
                                        ft.Text("Cadastrar Novo Ambiente 🏠", size=26, weight="bold", color="#1E3D59")
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Divider(),
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
                spacing=20
            )
        ],
        padding=20,
        bgcolor="#F5F5F5"
    )


# --------------------------------------------------------------------
# 📋 Página de LISTAGEM
# --------------------------------------------------------------------
def ambiente_listar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/ambiente/listar", controls=[])

    user = SessionManager.get_current_user()
    controller = AmbienteController()

    tabela = ft.Column(spacing=10)

    # Voltar
    def voltar_click(e):
        page.go("/dashboard")

    # Carregar tabela
    def carregar_lista():
        ambientes = controller.listar_ambientes(user["id"])
        tabela.controls.clear()

        if not ambientes:
            tabela.controls.append(ft.Text("Nenhum ambiente encontrado.", color="gray"))
        else:
            for amb in ambientes:
                tabela.controls.append(
                    ft.Row(
                        [
                            ft.Text(f"{amb.ambiente_nome}", width=200, weight="bold"),
                            ft.Text(amb.ambiente_descricao or "-", width=250),
                            ft.Text(str(amb.ambiente_dt_criacao)[:16], width=160),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
        page.update()

    carregar_lista()

    return ft.View(
        route="/ambiente/listar",
        controls=[
            ft.Row(
                controls=[
                    barra_lateral(user, page, "listar"),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            tooltip="Voltar ao dashboard",
                                            on_click=voltar_click
                                        ),
                                        ft.Text("Ambientes Cadastrados 🏠", size=26, weight="bold", color="#1E3D59")
                                    ],
                                    alignment=ft.MainAxisAlignment.START
                                ),
                                ft.Divider(),
                                tabela
                            ],
                            spacing=15,
                            expand=True
                        ),
                        expand=True,
                        padding=ft.padding.all(30),
                        bgcolor="#FAFAFA",
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=8, color="#E0E0E0")
                    )
                ],
                expand=True,
                spacing=20
            )
        ],
        padding=20,
        bgcolor="#F5F5F5"
    )
