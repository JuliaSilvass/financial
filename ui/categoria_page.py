import flet as ft
from services.session_manager import SessionManager
from controllers.categoria_controller import CategoriaController
from utils.sidebar import build_sidebar
from utils.dialogs import show_confirm_dialog, show_alert
from utils.list_page import build_list_page
from utils.search_bar import build_search_bar


# ==========================================================
# Sidebar 
# ==========================================================
def categoria_sidebar(page, user, active_route:str):
    menu_items = [
        {"label": "Listar categorias", "route": "/categoria/listar", "icon": ft.Icons.LIST},
        {"label": "Cadastrar categoria", "route": "/categoria/cadastrar", "icon": ft.Icons.ADD},
    ]
    return build_sidebar(
        page=page,
        user=user,
        menu_items=menu_items,
        active_route=active_route
    )


# --------------------------------------------------------------------
# LISTAR CATEGORIAS
# --------------------------------------------------------------------
def categoria_listar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/categoria/listar", controls=[])

    user = SessionManager.get_current_user()
    controller = CategoriaController()

    sidebar  = categoria_sidebar(page, user, "/categoria/listar")

    categorias = controller.listar_categoria(user["id"])
    columns = [
        {"label": "Nome", "field": "categoria_nome", "width": 200},
    ]

    def on_click(cat):
        page.go(f"/categoria/detalhar/{cat.categoria_id}")

    # --------------------------------------------------
    # Tabela (variável que será atualizada)
    # --------------------------------------------------
    tabela = build_list_page(
        items=categorias,
        columns=columns,
        on_item_click=on_click,
    )

    # --------------------------------------------------
    # Busca 
    # --------------------------------------------------
    def on_search(texto):
        texto = texto.lower()
        filtrados = [
            cat for cat in categorias
            if texto in cat.categoria_nome.lower()
        ]

        nova_tabela = build_list_page(
            items=filtrados,
            columns=columns,
            on_item_click=on_click,
            search_bar=search_bar,  # mantém a barra
        )

        tabela.controls.clear()
        tabela.controls.extend(nova_tabela.controls)
        page.update()

    search_bar = build_search_bar(
        hint_text="Pesquisar categorias...",
        on_change=on_search
    )

    # --------------------------------------------------
    # Recria tabela com search bar
    # --------------------------------------------------
    tabela = build_list_page(
        items=categorias,
        columns=columns,
        on_item_click=on_click,
        search_bar=search_bar,
    )

    def voltar_click(e):
        page.go("/dashboard")

    return ft.View(
        route="/categoria/listar",
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
                        padding=ft.padding.all(30),
                        bgcolor="#FAFAFA",
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=8, color="#E0E0E0"),
                        content=ft.Column(
                            expand=True,
                            spacing=15,
                            controls=[
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            tooltip="Voltar ao dashboard",
                                            on_click=voltar_click
                                        ),
                                        ft.Text(
                                                "Categorias cadastradas", 
                                                size=26, 
                                                weight="bold"
                                            ),
                                    ]
                                ),
                                ft.Divider(),
                                tabela
                            ],
                        ),
                    ),
                ],
            )
        ],
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

    sidebar = categoria_sidebar(page, user, "/categoria/cadastrar")

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
                    sidebar,
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

    sidebar  = categoria_sidebar(page, user, "/categoria/listar")

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
                    sidebar,
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
