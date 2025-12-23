import flet as ft
from services.session_manager import SessionManager
from controllers.ambiente_controller import AmbienteController
from utils.sidebar import build_sidebar
from utils.dialogs import show_confirm_dialog, show_alert

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
    tabela = ft.Column(spacing=10)

    sidebar = ambiente_sidebar(page, user, "/ambiente/listar")

    def voltar_click(e):
        page.go("/dashboard")

    def carregar_lista():
        tabela.controls.clear()
        ambientes = controller.listar_ambientes(user["id"])

        if not ambientes:
            tabela.controls.append(ft.Text("Nenhum ambiente encontrado.", color="gray"))
        else:
            for amb in ambientes:
                tabela.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(amb.ambiente_nome, width=200, weight="bold"),
                                ft.Text(amb.ambiente_descricao or "-", width=250),
                                ft.Text(str(amb.ambiente_dt_criacao)[:16], width=160),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=ft.padding.symmetric(vertical=10, horizontal=15),
                        border_radius=8,
                        bgcolor="#F1F8E9",
                        on_click=lambda e, a_id=amb.ambiente_id: page.go(
                            f"/ambiente/detalhar/{a_id}"
                        ),
                    )
                )
        page.update()

    carregar_lista()

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
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
