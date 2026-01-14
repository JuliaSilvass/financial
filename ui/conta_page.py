import flet as ft
from services.session_manager import SessionManager
from controllers.conta_controller import ContaController
from utils.sidebar import build_sidebar
from utils.dialogs import show_confirm_dialog, show_alert
from utils.list_page import build_list_page
from utils.search_bar import build_search_bar
from utils.replace import to_float


# --------------------------------------------------------------------
# sidebar 
# --------------------------------------------------------------------
def conta_sidebar(page, user, active_route:str):
    menu_items = [
        {"label": "Listar Contas", "route": "/conta/listar", "icon": ft.Icons.LIST},
        {"label": "Cadastrar Conta", "route": "/conta/cadastrar", "icon": ft.Icons.ADD},
    ]
    return build_sidebar(
        page=page,
        user=user,
        menu_items=menu_items,
        active_route=active_route
    )

# --------------------------------------------------------------------
# LISTAR CONTAS
# --------------------------------------------------------------------
def conta_listar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/conta/listar", controls=[])

    user = SessionManager.get_current_user()
    controller = ContaController()

    sidebar = conta_sidebar(page, user, "/conta/listar")

    contas = controller.listar_conta(user["id"])
    columns = [
        {"label": "Nome", "field": "conta_nome", "width": 200},
        {"label": "Tipo", "field": "conta_tipo", "width": 200},
        {"label": "Saldo Inicial", "field": "conta_saldo_limite_inicial", "width": 150},
        {"label": "Saldo Disponível", "field": "conta_saldo_limite_disponivel", "width": 150},
        {"label": "Status", "field": "conta_ativo", "width": 100},
        {"label": "Criado em", "field": "conta_dt_criacao", "width": 160, "type": "date"}
    ]   

    def on_click(conta):
        page.go(f"/conta/detalhar/{conta.conta_id}")

    # --------------------------------
    # Tabela (variavel que será atualizada)
    # ----------------------------------------
    tabela = build_list_page(
        items=contas,
        columns=columns,
        on_item_click=on_click,
    )

    # --------------------------------------------------
    # Busca
    # --------------------------------------------------

    def on_search(texto):
        texto = texto.lower()

        filtrados = [
            conta for conta in contas
            if texto in conta.conta_nome.lower() or
               (conta.conta_tipo and texto in conta.conta_tipo.lower())
        ]

        nova_tabela = build_list_page(
            items=filtrados,
            columns=columns,
            on_item_click=on_click,
            search_bar=search_bar,
        )

        tabela.controls.clear()
        tabela.controls.extend(nova_tabela.controls)
        page.update()
    
    search_bar = build_search_bar(
        hint_text="Pesquisar contas...",
        on_change=on_search,
    )

    # --------------------------------------------------
    # Recria tabela com search bar
    # --------------------------------------------------
    tabela = build_list_page(
        items=contas,
        columns=columns,
        on_item_click=on_click,
        search_bar=search_bar,
    )

    def voltar_click(e):
        page.go("/dashboard")

    return ft.View(
        route="/conta/listar",
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
                                            on_click=voltar_click),
                                        ft.Text(
                                            "Contas Cadastradas", 
                                            size=26, 
                                            weight="bold", 
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
# CADASTRAR CONTA   
# --------------------------------------------------------------------
def conta_cadastrar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/conta/cadastrar", controls=[])

    user = SessionManager.get_current_user()
    controller = ContaController()

    sidebar = conta_sidebar(page, user, "/conta/cadastrar")

    nome_field = ft.TextField(
        label="Nome da Conta", 
        width=400,
        hint_text="Ex: Banco Legal"
        )
    tipo_field = ft.Dropdown(
        label="Tipo de Conta",
        width=400,
        options=[
            ft.dropdown.Option("Corrente", "Conta Corrente"),
            ft.dropdown.Option("Poupança", "Poupança"),
            ft.dropdown.Option("Investimento", "Investimento"),
            ft.dropdown.Option("Cartão de Crédito", "Cartão de Crédito"),
            ft.dropdown.Option("Carteira", "Carteira"),
            ft.dropdown.Option("Outros", "Outros"),
        ]
    )
    saldo_inicial_field = ft.TextField(
        label="Saldo Inicial", 
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9.,]"),
        hint_text="Ex: 1500,00"
    )
    saldo_disponivel_field = ft.TextField(
        label="Saldo Disponível", 
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9.,]"),
        hint_text="Ex: 1500,00"
    )
    ativo_field = ft.CupertinoSwitch(
        value=True
    )

    ativo_container = ft.Container(
        width=400,
        padding=ft.padding.symmetric(vertical=6),
        content=ft.Row(
            [
                ft.Text(
                    "Conta Ativa",
                    size=16,
                    weight="bold",
                    color="#1E3D59"
                ),
                ativo_field
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    mensagem = ft.Text()

    def voltar_click(e):
        page.go("/conta/listar")

    def salvar_click(e):
        nome = nome_field.value.strip()
        tipo = tipo_field.value
        saldo_inicial = to_float(saldo_inicial_field.value)
        saldo_disponivel = to_float(saldo_disponivel_field.value)
        conta_ativo = ativo_field.value

        if not nome or not tipo:
            show_alert(
                page,
                "Campo obrigatório",
                "Nome e tipo da conta são obrigatórios."
            )
            return
        
        ok, msg = controller.register_conta(nome, tipo, saldo_inicial, saldo_disponivel, conta_ativo, user["id"])

        if ok:
            page.go("/conta/listar")
        else:
            show_alert(
                page,
                "Erro ao cadastrar conta",
                msg)

        page.update()

    return ft.View(
        route="/conta/cadastrar",
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
                                            tooltip="Voltar", 
                                            on_click=voltar_click
                                        ),
                                        ft.Text(
                                            "Detalhes da Conta", 
                                            size=26, 
                                            weight="bold"
                                        ),
                                    ]
                                ),
                                ft.Divider(),
                                nome_field,
                                tipo_field,
                                saldo_inicial_field,
                                saldo_disponivel_field,
                                ativo_container,
                                ft.ElevatedButton(
                                    text="Salvar Conta",
                                    icon=ft.Icons.SAVE,
                                    bgcolor="#44CFA1",
                                    color="white",
                                    on_click=salvar_click
                                ),
                                mensagem,
                            ],
                        ),
                    )
                ],
            )
        ],
    )


# --------------------------------------------------------------------
# DETALHAR / EDITAR / EXCLUIR CONTA
# --------------------------------------------------------------------
def conta_detalhar_page(page: ft.Page, conta_id: int):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route=f"/conta/detalhar/{conta_id}", controls=[])

    user = SessionManager.get_current_user()
    controller = ContaController()
    conta = controller.get_conta(conta_id)

    if not conta:
        show_alert(
            page,
            "Conta não encontrada",
            "A conta solicitada não foi encontrada ou não existe."
        )
        page.go("/conta/listar")
        return
    
    sidebar = conta_sidebar(page, user, "/conta/listar")

    nome_field = ft.TextField(
        label="Nome da Conta", 
        width=400, 
        value=conta.conta_nome
        )
    tipo_field = ft.Dropdown(
        label="Tipo de Conta",
        width=400,
        value=conta.conta_tipo,
        options=[
            ft.dropdown.Option("Corrente", "Conta Corrente"),
            ft.dropdown.Option("Poupança", "Poupança"),
            ft.dropdown.Option("Investimento", "Investimento"),
            ft.dropdown.Option("Cartão de Crédito", "Cartão de Crédito"),
            ft.dropdown.Option("Carteira", "Carteira"),
            ft.dropdown.Option("Outros", "Outros"),
        ]
    )
    saldo_inicial_field = ft.TextField(
        label="Saldo Inicial", 
        width=400, 
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9.,]"),
        value=str(conta.conta_saldo_limite_inicial)
    )
    saldo_disponivel_field = ft.TextField(
        label="Saldo Disponível", 
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9.,]"), 
        value=str(conta.conta_saldo_limite_disponivel)
    )
    ativo_field = ft.CupertinoSwitch(
        value=conta.conta_ativo
    )
    mensagem = ft.Text()

    ativo_container = ft.Container(
        width=400,
        padding=ft.padding.symmetric(vertical=6),
        content=ft.Row(
            [
                ft.Text(
                    "Conta Ativa",
                    size=16,
                    weight="bold",
                    color="#1E3D59"
                ),
                ativo_field
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    def voltar_click(e):
        page.go("/conta/listar")

    def salvar_click(e):
        nome = nome_field.value.strip()
        tipo = tipo_field.value
        saldo_inicial = to_float(saldo_inicial_field.value)
        saldo_disponivel = to_float(saldo_disponivel_field.value)
        ativo = ativo_field.value

        if not nome or not tipo:
                show_alert(
                    page,
                    "Campo obrigatório",
                    "Nome e tipo da conta são obrigatórios."
                )
                return

        ok, msg = controller.update_conta(conta_id, nome, tipo, saldo_inicial, saldo_disponivel, ativo)
        
        if ok: 
            show_alert(page, "Sucesso", msg)
        else: 
            show_alert(page, "Erro", msg)

    def excluir_click(e):
        def confirmar_excluir():
            ok, msg = controller.delete_conta(conta_id)
            if ok:
                page.go("/conta/listar")
            else:
                show_alert(page, "Erro", msg)
    
        show_confirm_dialog(
            page,
            title="Confirmar exclusão",
            message="Tem certeza que deseja excluir esta conta? Esta ação é irreversível.",
            on_confirm=confirmar_excluir
        )

        # bs = ft.BottomSheet(
        #     ft.Container(
        #         ft.Column([
        #             ft.Text("Confirmar exclusão", weight="bold", size=18),
        #             ft.Text("Tem certeza que deseja excluir esta conta? Esta ação é irreversível."),
        #             ft.Row([
        #                 ft.TextButton("Cancelar", on_click=lambda ev: (setattr(bs, "open", False), page.update())),
        #                 ft.TextButton("Excluir", on_click=confirmar_excluir, style=ft.ButtonStyle(color="red")),
        #             ], alignment=ft.MainAxisAlignment.END)
        #         ]),
        #         padding=20,
        #     ),
        #     open=True,
        # )
        # page.overlay.append(bs)
        # page.update()

    return ft.View(
        route=f"/conta/detalhar/{conta_id}",
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
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK, 
                                        tooltip="Voltar", 
                                        on_click=voltar_click
                                        ),
                                    ft.Text(
                                        "Detalhes da Conta", 
                                        size=26, 
                                        weight="bold"
                                        ),
                                    ]
                                ),
                                ft.Divider(),
                                nome_field,
                                tipo_field,
                                saldo_inicial_field,
                                saldo_disponivel_field,
                                ativo_container,
                                ft.Row([
                                    ft.ElevatedButton(
                                        text="Salvar Alterações", 
                                        icon=ft.Icons.SAVE, 
                                        bgcolor="#44CFA1", 
                                        color="white", 
                                        on_click=salvar_click
                                        ),
                                    ft.ElevatedButton(
                                        text="Excluir Conta", 
                                        icon=ft.Icons.DELETE, 
                                        on_click=excluir_click
                                    ),
                                ], 
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                mensagem,
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )
