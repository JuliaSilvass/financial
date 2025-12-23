import flet as ft
from services.session_manager import SessionManager
from controllers.ambiente_controller import AmbienteController
from utils.sidebar import build_sidebar
from utils.dialogs import show_confirm_dialog, show_alert
from utils.list_page import build_list_page
from utils.search_bar import build_search_bar

# ==========================================================
# Sidebar 
# ==========================================================
def ambiente_sidebar(page, user, active_route: str):
    menu_items = [
        {"label": "Listar Ambientes", "route": "/ambiente/listar", "icon": ft.Icons.LIST},
        {"label": "Cadastrar Novo", "route": "/ambiente/cadastrar", "icon": ft.Icons.ADD},
    ]
    return build_sidebar(
        page=page,
        user=user,
        menu_items=menu_items,
        active_route=active_route
    )


# ==========================================================
# LISTAR AMBIENTES
# ==========================================================
def ambiente_listar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/ambiente/listar", controls=[])

    user = SessionManager.get_current_user()
    controller = AmbienteController()

    sidebar = ambiente_sidebar(page, user, "/ambiente/listar")

    ambientes = controller.listar_ambientes(user["id"])
    columns = [
        {"label": "Nome", "field": "ambiente_nome", "width": 200},
        {"label": "Descrição", "field": "ambiente_descricao", "width": 250},
        {
            "label": "Criado em",
            "field": "ambiente_dt_criacao",
            "width": 160,
            "type": "date",
        },
    ]

    def on_click(amb):
        page.go(f"/ambiente/detalhar/{amb.ambiente_id}")

    # --------------------------------------------------
    # Tabela (variável que será atualizada)
    # --------------------------------------------------
    tabela = build_list_page(
        items=ambientes,
        columns=columns,
        on_item_click=on_click,
    )

    # --------------------------------------------------
    # Busca
    # --------------------------------------------------
    def on_search(texto):
        texto = texto.lower()

        filtrados = [
            amb for amb in ambientes
            if texto in amb.ambiente_nome.lower()
            or (amb.ambiente_descricao and texto in amb.ambiente_descricao.lower())
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
        hint_text="Pesquisar ambientes...",
        on_change=on_search,
    )

    # --------------------------------------------------
    # Recria tabela com search bar
    # --------------------------------------------------
    tabela = build_list_page(
        items=ambientes,
        columns=columns,
        on_item_click=on_click,
        search_bar=search_bar,
    )


    def voltar_click(e):
        page.go("/dashboard")

    return ft.View(
        route="/ambiente/listar",
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
                                            on_click=voltar_click,
                                        ),
                                        ft.Text(
                                            "Ambientes Cadastrados",
                                            size=26, 
                                            weight="bold",
                                        ),
                                    ]
                                ),
                                ft.Divider(),
                                tabela,
                            ],
                        ),
                    ),
                ],
            )
        ],
    )



# ==========================================================
# CADASTRAR AMBIENTE
# ==========================================================
def ambiente_cadastrar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/ambiente/cadastrar", controls=[])

    user = SessionManager.get_current_user()
    controller = AmbienteController()

    sidebar = ambiente_sidebar(page, user, "/ambiente/cadastrar")

    nome_field = ft.TextField(label="Nome do Ambiente", width=400)
    desc_field = ft.TextField(label="Descrição", multiline=True, width=400)
    mensagem = ft.Text()

    def voltar_click(e):
        page.go("/ambiente/listar")

    def salvar_click(e):
        nome = nome_field.value.strip()
        descricao = desc_field.value.strip()

        if not nome:
            show_alert(
                page,
                "Campo obrigatório",
                "O nome do ambiente é obrigatório."
            )
            return
        
        ok, msg = controller.register_ambiente(nome, descricao, user["id"])

        if ok:
            page.go("/ambiente/listar")
        else:
            show_alert(page, "Erro ao salvar", msg)
        
        page.update()

    return ft.View(
        route="/ambiente/cadastrar",
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
                        shadow=ft.BoxShadow(blur_radius=8, color="#E0E0E0"),
                        content=ft.Column(
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            on_click=voltar_click,
                                        ),
                                        ft.Text(
                                            "Cadastrar Novo Ambiente",
                                            size=26,
                                            weight="bold",
                                        ),
                                    ]
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
                                ),
                                mensagem,
                            ],
                        ),
                    ),
                ],
            )
        ],
    )


# ==========================================================
# DETALHAR / EDITAR / EXCLUIR AMBIENTE
# ==========================================================
def ambiente_detalhar_page(page: ft.Page, ambiente_id: int):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route=f"/ambiente/detalhar/{ambiente_id}", controls=[])

    user = SessionManager.get_current_user()
    controller = AmbienteController()
    ambiente = controller.get_ambiente(ambiente_id)

    if not ambiente:
        page.go("/ambiente/listar")
        return

    sidebar = ambiente_sidebar(page, user, "/ambiente/listar")

    nome_field = ft.TextField(
        label="Nome do Ambiente",
        width=400,
        value=ambiente.ambiente_nome,
    )
    desc_field = ft.TextField(
        label="Descrição",
        multiline=True,
        width=400,
        value=ambiente.ambiente_descricao,
    )
    mensagem = ft.Text()

    def voltar_click(e):
        page.go("/ambiente/listar")

    def salvar_click(e):
        nome = nome_field.value.strip()
        descricao = desc_field.value.strip()
        
        if not nome:
            show_alert(
                page,
                "Campo obrigatório",
                "O nome do ambiente é obrigatório."
            )
            return

        ok, msg = controller.update_ambiente(ambiente_id, nome, descricao)

        if ok:
            show_alert(page, "Sucesso", msg)
        else:
            show_alert(page, "Erro", msg)

    def excluir_click(e):

        def confirmar_exclusao():
            ok, msg = controller.delete_ambiente(ambiente_id)
            if ok:
                page.go("/ambiente/listar")
            else:
                show_alert(page, "Erro", msg)
        
        show_confirm_dialog(
            page, 
            title="Confirmar Exclusão",
            message="Tem certeza que deseja excluir este ambiente? Esta ação não pode ser desfeita.",
            on_confirm=confirmar_exclusao
        )

    return ft.View(
        route=f"/ambiente/detalhar/{ambiente_id}",
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
                        shadow=ft.BoxShadow(blur_radius=8, color="#E0E0E0"),
                        content=ft.Column(
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            on_click=voltar_click,
                                        ),
                                        ft.Text(
                                            "Detalhes do Ambiente",
                                            size=26,
                                            weight="bold",
                                        ),
                                    ]
                                ),
                                ft.Divider(),
                                nome_field,
                                desc_field,
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "Salvar Alterações",
                                            icon=ft.Icons.SAVE,
                                            bgcolor="#44CFA1",
                                            color="white",
                                            on_click=salvar_click,
                                        ),
                                        ft.OutlinedButton(
                                            "Excluir Ambiente",
                                            icon=ft.Icons.DELETE,
                                            on_click=excluir_click,
                                        ),
                                    ],
                                    spacing=15,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                mensagem,
                            ],
                        ),
                    ),
                ],
            )
        ],
    )
