import flet as ft
from services.session_manager import SessionManager
from controllers.categoria_controller import CategoriaController
from utils.sidebar import build_sidebar
from utils.dialogs import show_confirm_dialog, show_alert
from utils.list_page import build_list_page
from utils.search_bar import build_search_bar

# ----------------------------------------------------------
# Barra lateral padrão
# ----------------------------------------------------------
def barra_lateral(user, page, current_page):
    def go_to_listar(e):
        if current_page != "listar":
            page.go("/categoria/listar")

    def go_to_cadastrar(e):
        if current_page != "cadastrar":
            page.go("/categoria/cadastrar")

    def logout_click(e):
        SessionManager.logout()
        page.go("/")

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(f"Olá, {user['nome']}", size=20, weight="bold", color="#1E3D59"),
                    padding=ft.padding.only(bottom=10)
                ),
                ft.Divider(height=2, thickness=1, color="#44CFA1"),
                ft.ElevatedButton(
                    text="Listar categorias",
                    icon=ft.Icons.LIST,
                    bgcolor="#44CFA1" if current_page == "listar" else "#B2DFDB",
                    color="white" if current_page == "listar" else "#1E3D59",
                    on_click=go_to_listar if current_page != "listar" else None,
                    disabled=current_page == "listar",
                    expand=True
                ),
                ft.ElevatedButton(
                    text="Cadastrar nova categoria",
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
# Página de LISTAGEM
# --------------------------------------------------------------------
def categoria_listar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/categoria/listar", controls=[])

    user = SessionManager.get_current_user()
    controller = CategoriaController()
    tabela = ft.Column(spacing=10)

    def voltar_click(e):
        page.go("/dashboard")

    def carregar_lista():
        categoria = controller.listar_categoria(user["id"])
        tabela.controls.clear()

        if not categoria:
            tabela.controls.append(ft.Text("Nenhuma categoria encontrada.", color="gray"))
        else:
            for cat in categoria:
                linha = ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{cat.categoria_nome}", width=200, weight="bold"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                    border_radius=8,
                    bgcolor="#F1F8E9",
                    on_click=lambda e, a_id=cat.categoria_id: page.go(f"/categoria/detalhar/{a_id}")
                )
                linha.hover_color = "#C8E6C9"
                tabela.controls.append(linha)
        page.update()

    carregar_lista()

    return ft.View(
        route="/categoria/listar",
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
                                        ft.Text("Categorias cadastradas", size=26, weight="bold", color="#1E3D59")
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
                        shadow=ft.BoxShadow(blur_radius=8, color="#E0E0E0"),
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
# Página de CADASTRO
# --------------------------------------------------------------------
def categoria_cadastrar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/categoria/cadastrar", controls=[])

    user = SessionManager.get_current_user()
    controller = CategoriaController()

    nome_field = ft.TextField(label="Nome da categoria", width=400)
    mensagem = ft.Text()

    def voltar_click(e):
        page.go("/categoria/listar")

    def salvar_click(e):
        nome = nome_field.value.strip()

        if not nome:
            show_alert(
                page, 
                "Campo obrigatório", 
                "O nome da categoria é obrigatório."
            )
            return
        
        ok, msg = controller.register_categoria(nome, user["id"])

        if ok: 
            page.go("/categoria/listar")
        else:  
            show_alert(page, "Erro ao salvar", msg)
        page.update()

    return ft.View(
        route="/categoria/cadastrar",
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
                                        ft.Text("Cadastrar Nova Categoria", size=26, weight="bold", color="#1E3D59")
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Divider(),
                                nome_field,
                                ft.ElevatedButton(
                                    text="Salvar categoria",
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
# Página de DETALHES / EDIÇÃO / EXCLUSÃO
# --------------------------------------------------------------------
def categoria_detalhar_page(page: ft.Page, categoria_id: int):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route=f"/categoria/detalhar/{categoria_id}", controls=[])

    user = SessionManager.get_current_user()
    controller = CategoriaController()
    categoria = controller.get_categoria(categoria_id)

    if not categoria:
        show_alert(
                page, 
                "Categoria não encontrada", 
                "Categoria não encontrada."
            )
        page.go("/categoria/listar")
        return

    nome_field = ft.TextField(label="Nome da categoria", width=400, value=categoria.categoria_nome)
    mensagem = ft.Text()

    def voltar_click(e):
        page.go("/categoria/listar")

    def salvar_click(e):
        nome = nome_field.value.strip()

        if not nome: 
            show_alert(
                page, 
                "Campo obrigatório", 
                "O nome da categoria é obrigatório."
            )
            return    

        ok, msg = controller.update_categoria(categoria_id, nome, user["id"])

        if ok:
            show_alert(page, "Sucesso", msg)
        else:
            show_alert(page, "Erro", msg)

        page.update()

    def excluir_click(e):
        def confirmar_excluir():
            ok, msg = controller.delete_categoria(categoria_id)
            page.update()
            if ok:
                page.go("/categoria/listar")
            else:
                show_alert(page, "Erro", msg)

        show_confirm_dialog(
            page, 
            title="Confirmar Exclusão",
            message="Tem certeza que deseja excluir essa categoria? Esta ação não pode ser desfeita.",
            on_confirm=confirmar_excluir
        )


    return ft.View(
        route=f"/categoria/detalhar/{categoria_id}",
        controls=[
            ft.Row(
                controls=[
                    barra_lateral(user, page, "detalhar"),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    [
                                        ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", on_click=voltar_click),
                                        ft.Text("Detalhes da categoria", size=26, weight="bold", color="#1E3D59"),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Divider(),
                                nome_field,
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            text="Salvar Alterações",
                                            icon=ft.Icons.SAVE,
                                            bgcolor="#44CFA1",
                                            color="white",
                                            on_click=salvar_click,
                                        ),
                                        ft.OutlinedButton(
                                            "Excluir Categoria",
                                            icon=ft.Icons.DELETE,
                                            on_click=excluir_click,
                                        ),
                                    ],
                                    spacing=15,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                mensagem,
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                        padding=ft.padding.all(40),
                        bgcolor="#FAFAFA",
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=8, color="#E0E0E0"),
                    ),
                ],
                expand=True,
                spacing=20,
            ),
        ],
        padding=20,
        bgcolor="#F5F5F5",
    )
