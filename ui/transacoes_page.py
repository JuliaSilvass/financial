import flet as ft
from services.session_manager import SessionManager
from controllers.transacao_controller import TransacaoController


def barra_lateral(user, page, current_page):
    def go_to_listar(e):
        if current_page != "listar":
            page.go("/transacao/listar")

    def go_to_cadastrar(e):
        if current_page != "cadastrar":
            page.go("/transacao/cadastrar")

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
                    text="Listar Transações",
                    icon=ft.Icons.LIST,
                    bgcolor="#44CFA1" if current_page == "listar" else "#B2DFDB",
                    color="white" if current_page == "listar" else "#1E3D59",
                    on_click=go_to_listar if current_page != "listar" else None,
                    disabled=current_page == "listar",
                    expand=True
                ),
                ft.ElevatedButton(
                    text="Cadastrar Nova Transação",
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
def transacao_listar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/transacao/listar", controls=[])

    user = SessionManager.get_current_user()
    controller = TransacaoController()
    tabela = ft.Column(spacing=10)

    def voltar_click(e):
        page.go("/dashboard")

    def carregar_lista():
        transacoes = controller.listar_transacoes(user["id"])
        tabela.controls.clear()

        if not transacoes:
            tabela.controls.append(ft.Text("Nenhuma transação encontrada.", color="gray"))
        else:
            for transacao in transacoes:
                linha = ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{transacao.conta_nome}", width=200, weight="bold"),
                            # ft.Text(transacao.conta_tipo or "-", width=200),
                            # ft.Text(f"R$ {transacao.conta_saldo_limite_inicial:.2f}", width=150),
                            # ft.Text(f"R$ {transacao.conta_saldo_limite_disponivel:.2f}", width=150),
                            # ft.Text("Ativa" if transacao.conta_ativo else "Inativa", width=100),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.symmetric(vertical=10, horizontal=15),
                    border_radius=8,
                    bgcolor="#F1F8E9",
                    on_click=lambda e, tid=transacao.transacao_id: page.go(f"/transacao/detalhar/{tid}")
                )
                linha.hover_color = "#C8E6C9"
                tabela.controls.append(linha)
        page.update()

    carregar_lista()

    return ft.View(
        route="/transacao/listar",
        controls=[
            ft.Row(
                controls=[
                    barra_lateral(user, page, "listar"),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    [
                                        ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", on_click=voltar_click),
                                        ft.Text("Transações Cadastradas", size=26, weight="bold", color="#1E3D59")
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
def transacao_cadastrar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/transacao/cadastrar", controls=[])

    user = SessionManager.get_current_user()
    controller = TransacaoController()

    nome_field = ft.TextField(label="Nome da Transacao", width=400)
    # tipo_field = ft.Dropdown(
    #     label="Tipo de Transação",
    #     width=400,
    #     options=[
    #         ft.dropdown.Option("corrente", "Conta Corrente"),
    #         ft.dropdown.Option("poupanca", "Poupança"),
    #         ft.dropdown.Option("investimento", "Investimento"),
    #         ft.dropdown.Option("cartao_credito", "Cartão de Crédito"),
    #         ft.dropdown.Option("carteira", "Carteira"),
    #         ft.dropdown.Option("outros", "Outros"),
    #     ]
    # )
    # saldo_inicial_field = ft.TextField(label="Saldo Inicial", width=400)
    # saldo_disponivel_field = ft.TextField(label="Saldo Disponível", width=400)
    # ativo_field = ft.Checkbox(label="Conta Ativa", value=True)
    mensagem = ft.Text(color="green")

    def to_float(value):
        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return 0.0

    def voltar_click(e):
        page.go("/transacao/listar")

    def salvar_click(e):
        nome = nome_field.value.strip()
        # tipo = tipo_field.value
        # saldo_inicial = to_float(saldo_inicial_field.value)
        # saldo_disponivel = to_float(saldo_disponivel_field.value)
        # conta_ativo = ativo_field.value

        if not nome:
            mensagem.value = "Nome da transação é obrigatório."
            mensagem.color = "red"
        else:
            ok, msg = controller.register_transacao(nome, user["id"])
            mensagem.value = msg
            mensagem.color = "green" if ok else "red"

            if ok:
                nome_field.value = ""
                # tipo_field.value = None
                # saldo_inicial_field.value = ""
                # saldo_disponivel_field.value = ""
                # ativo_field.value = True
                page.snack_bar = ft.SnackBar(ft.Text("Transação cadastrada com sucesso!"))
                page.snack_bar.open = True
                page.go("/transacao/listar")
        page.update()

    return ft.View(
        route="/transacao/cadastrar",
        controls=[
            ft.Row(
                controls=[
                    barra_lateral(user, page, "cadastrar"),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", on_click=voltar_click),
                                    ft.Text("Cadastrar Nova transação", size=26, weight="bold", color="#1E3D59")
                                ]),
                                ft.Divider(),
                                nome_field,
                                # tipo_field,
                                # saldo_inicial_field,
                                # saldo_disponivel_field,
                                # ativo_field,
                                ft.ElevatedButton(
                                    text="Salvar transação",
                                    icon=ft.Icons.SAVE,
                                    bgcolor="#44CFA1",
                                    color="white",
                                    on_click=salvar_click
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
def transacao_detalhar_page(page: ft.Page, transacao_id: int):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route=f"/transacao/detalhar/{transacao_id}", controls=[])

    user = SessionManager.get_current_user()
    controller = TransacaoController()
    transacao = controller.get_transacao(transacao_id)

    if not transacao:
        page.snack_bar = ft.SnackBar(ft.Text("Transacao não encontrada."))
        page.snack_bar.open = True
        page.go("/transacao/listar")
        return

    nome_field = ft.TextField(label="Nome da transacao", width=400, value=transacao.transacao_nome)
    # tipo_field = ft.Dropdown(
    #     label="Tipo de Conta",
    #     width=400,
    #     value=conta.conta_tipo,
    #     options=[
    #         ft.dropdown.Option("corrente", "Conta Corrente"),
    #         ft.dropdown.Option("poupanca", "Poupança"),
    #         ft.dropdown.Option("investimento", "Investimento"),
    #         ft.dropdown.Option("cartao_credito", "Cartão de Crédito"),
    #         ft.dropdown.Option("carteira", "Carteira"),
    #         ft.dropdown.Option("outros", "Outros"),
    #     ]
    # )
    # saldo_inicial_field = ft.TextField(label="Saldo Inicial", width=400, value=str(conta.conta_saldo_limite_inicial))
    # saldo_disponivel_field = ft.TextField(label="Saldo Disponível", width=400, value=str(conta.conta_saldo_limite_disponivel))
    # ativo_field = ft.Checkbox(label="Conta Ativa", value=conta.conta_ativo)
    mensagem = ft.Text(color="green")

    def to_float(value):
        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return 0.0

    def voltar_click(e):
        page.go("/transacao/listar")

    def salvar_click(e):
        nome = nome_field.value.strip()
        # tipo = tipo_field.value
        # saldo_inicial = to_float(saldo_inicial_field.value)
        # saldo_disponivel = to_float(saldo_disponivel_field.value)
        # ativo = ativo_field.value

        ok, msg = controller.update_transacao(transacao_id, nome)
        mensagem.value = msg
        mensagem.color = "green" if ok else "red"
        page.update()

    def excluir_click(e):
        def confirmar_excluir(ev):
            ok, msg = controller.delete_transacao(transacao_id)
            bs.open = False
            page.update()
            if ok:
                page.snack_bar = ft.SnackBar(ft.Text("transacao excluída com sucesso!"))
                page.snack_bar.open = True
                page.go("/transacao/listar")
            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {msg}"))
                page.snack_bar.open = True
            page.update()

        bs = ft.BottomSheet(
            ft.Container(
                ft.Column([
                    ft.Text("Confirmar exclusão", weight="bold", size=18),
                    ft.Text("Tem certeza que deseja excluir esta transacao? Esta ação é irreversível."),
                    ft.Row([
                        ft.TextButton("Cancelar", on_click=lambda ev: (setattr(bs, "open", False), page.update())),
                        ft.TextButton("Excluir", on_click=confirmar_excluir, style=ft.ButtonStyle(color="red")),
                    ], alignment=ft.MainAxisAlignment.END)
                ]),
                padding=20,
            ),
            open=True,
        )
        page.overlay.append(bs)
        page.update()

    return ft.View(
        route=f"/transacao/detalhar/{transacao_id}",
        controls=[
            ft.Row(
                controls=[
                    barra_lateral(user, page, "detalhar"),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Voltar", on_click=voltar_click),
                                    ft.Text("Detalhes da transação", size=26, weight="bold", color="#1E3D59"),
                                ]),
                                ft.Divider(),
                                nome_field,
                                # tipo_field,
                                # saldo_inicial_field,
                                # saldo_disponivel_field,
                                # ativo_field,
                                ft.Row([
                                    ft.ElevatedButton(text="Salvar Alterações", icon=ft.Icons.SAVE, bgcolor="#44CFA1", color="white", on_click=salvar_click),
                                    ft.ElevatedButton(text="Excluir transação", icon=ft.Icons.DELETE, bgcolor="#F28B82", color="white", on_click=excluir_click),
                                ], spacing=15),
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
