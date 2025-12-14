import flet as ft
from services.session_manager import SessionManager
from controllers.transacao_controller import TransacaoController
from controllers.ambiente_controller import AmbienteController
from controllers.categoria_controller import CategoriaController
from controllers.conta_controller import ContaController
# from controllers.meta_controller import MetaController

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
                            ft.Text(f"ID Conta: {transacao.conta_id}", width=150, weight="bold"),
                            ft.Text(f"Valor: R$ {float(transacao.transacao_valor):.2f}", width=150),
                            ft.Text(f"Tipo: {transacao.transacao_tipo}", width=120),
                            ft.Text(f"Data: {transacao.transacao_data}", width=150),
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

    ambienteController = AmbienteController()
    categoriaController = CategoriaController()
    contaController = ContaController()
    # metaController = MetaController()

    ambientes = ambienteController.listar_ambientes(user["id"])
    categorias = categoriaController.listar_categoria(user["id"])
    contas = contaController.listar_conta(user["id"])
    # metas = metaController.listar_metas(user["id"])

    # Campos principais
    descricao_field = ft.TextField(label="Descrição da Transação", width=400)
    valor_field = ft.TextField(label="Valor (R$)", width=400)
    data_field = ft.TextField(label="Data (AAAA-MM-DD)", width=400)
    tipo_field = ft.Dropdown(
        label="Tipo da Transação",
        width=400,
        options=[
            ft.dropdown.Option("receita", "Receita"),
            ft.dropdown.Option("despesa", "Despesa"),
        ]
    )
    modo_field = ft.Dropdown(
        label="Modo de Pagamento",
        width=400,
        options=[
            ft.dropdown.Option("pix", "PIX"),
            ft.dropdown.Option("dinheiro", "Dinheiro"),
            ft.dropdown.Option("debito", "Débito"),
            ft.dropdown.Option("credito", "Crédito"),
            ft.dropdown.Option("TED", "TED"),
            ft.dropdown.Option("DOC", "DOC"),
            ft.dropdown.Option("outros", "Outros"),
        ]
    )
    ambiente_field = ft.Dropdown(
    label="Ambiente",
    width=400,
    options=[ft.dropdown.Option(str(a.ambiente_id), a.ambiente_nome) for a in ambientes],
    )

    categoria_field = ft.Dropdown(
        label="Categoria",
        width=400,
        options=[ft.dropdown.Option(str(c.categoria_id), c.categoria_nome) for c in categorias],
    )

    conta_field = ft.Dropdown(
        label="Conta",
        width=400,
        options=[ft.dropdown.Option(str(ct.conta_id), ct.conta_nome) for ct in contas],
    )

    # meta_field (opcional, deixar comentado por enquanto)
    # meta_field = ft.Dropdown(
    #     label="Meta (opcional)",
    #     width=400,
    #     options=[ft.dropdown.Option(str(m.meta_id), m.meta_nome) for m in metas],
    # )

    pago_field = ft.Checkbox(label="Pago", value=True)
    mensagem = ft.Text(color="green")

    def to_float(value):
        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return 0.0

    def voltar_click(e):
        page.go("/transacao/listar")

    def salvar_click(e):
        descricao = descricao_field.value.strip()
        valor = to_float(valor_field.value)
        data = data_field.value.strip()
        tipo = tipo_field.value
        modo = modo_field.value
        ambiente_id = ambiente_field.value
        categoria_id = categoria_field.value
        conta_id = conta_field.value
        # meta_id = meta_field.value if meta_field.value else None
        pago = pago_field.value

        if not descricao or valor <= 0 or not data or not tipo or not modo or not ambiente_id or not categoria_id or not conta_id:
            mensagem.value = "Preencha todos os campos obrigatórios."
            mensagem.color = "red"
        else:
            ok, msg = controller.register_transacao(
                descricao=descricao,
                valor=valor,
                data=data,
                ambiente_id=int(ambiente_id),
                categoria_id=int(categoria_id),
                conta_id=int(conta_id),
                tipo=tipo,
                modo=modo,
                pago=pago
            )
            mensagem.value = msg
            mensagem.color = "green" if ok else "red"

            if ok:
                descricao_field.value = ""
                valor_field.value = ""
                data_field.value = ""
                tipo_field.value = None
                modo_field.value = None
                ambiente_field.value = ""
                categoria_field.value = ""
                conta_field.value = ""
                pago_field.value = True

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
                                    ft.Text("Cadastrar Nova Transação", size=26, weight="bold", color="#1E3D59")
                                ]),
                                ft.Divider(),
                                descricao_field,
                                valor_field,
                                data_field,
                                tipo_field,
                                modo_field,
                                ambiente_field,
                                categoria_field,
                                conta_field,
                                # meta_field,
                                pago_field,

                                ft.ElevatedButton(
                                    text="Salvar Transação",
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
        page.snack_bar = ft.SnackBar(ft.Text("Transação não encontrada."))
        page.snack_bar.open = True
        page.go("/transacao/listar")
        return

    # --- Campos editáveis ---
    descricao_field = ft.TextField(label="Descrição", width=400, value=transacao.transacao_descricao)
    valor_field = ft.TextField(label="Valor (R$)", width=400, value=str(transacao.transacao_valor))
    tipo_field = ft.Dropdown(
        label="Tipo",
        width=400,
        value=transacao.transacao_tipo,
        options=[
            ft.dropdown.Option("receita", "Receita"),
            ft.dropdown.Option("despesa", "Despesa"),
        ]
    )
    modo_field = ft.Dropdown(
        label="Modo de Pagamento",
        width=400,
        value=transacao.transacao_modo,
        options=[
            ft.dropdown.Option("pix", "PIX"),
            ft.dropdown.Option("dinheiro", "Dinheiro"),
            ft.dropdown.Option("debito", "Débito"),
            ft.dropdown.Option("credito", "Crédito"),
            ft.dropdown.Option("TED", "TED"),
            ft.dropdown.Option("DOC", "DOC"),
            ft.dropdown.Option("outros", "Outros"),
        ]
    )
    pago_field = ft.Checkbox(label="Pago", value=transacao.transacao_pago)
    observacao_field = ft.TextField(label="Observação", width=400, value=transacao.transacao_observacao or "")
    local_field = ft.TextField(label="Local", width=400, value=transacao.transacao_local or "")
    dt_vencimento_field = ft.TextField(label="Data de Vencimento (AAAA-MM-DD)", width=400,
                                       value=str(transacao.transacao_dt_vencimento or "")[:10])

    mensagem = ft.Text(color="green")

    def to_float(value):
        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return 0.0

    def voltar_click(e):
        page.go("/transacao/listar")

    # --- SALVAR ALTERAÇÕES ---
    def salvar_click(e):
        descricao = descricao_field.value.strip()
        valor = to_float(valor_field.value)
        tipo = tipo_field.value
        modo = modo_field.value
        pago = pago_field.value
        observacao = observacao_field.value.strip()
        local = local_field.value.strip()
        dt_vencimento = dt_vencimento_field.value.strip()

        ok, msg = controller.update_transacao(
            transacao_id=transacao_id,
            descricao=descricao,
            valor=valor,
            tipo=tipo,
            modo=modo,
            pago=pago,
            observacao=observacao,
            local=local,
            dt_vencimento=dt_vencimento
        )
        mensagem.value = msg
        mensagem.color = "green" if ok else "red"
        page.update()

    # --- EXCLUIR TRANSACAO ---
    def excluir_click(e):
        def confirmar_excluir(ev):
            ok, msg = controller.delete_transacao(transacao_id)
            bs.open = False
            page.update()
            if ok:
                page.snack_bar = ft.SnackBar(ft.Text("Transação excluída com sucesso!"))
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
                    ft.Text("Tem certeza que deseja excluir esta transação? Esta ação é irreversível."),
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

    # --- VIEW FINAL ---
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
                                    ft.Text("Detalhes da Transação", size=26, weight="bold", color="#1E3D59"),
                                ]),
                                ft.Divider(),
                                descricao_field,
                                valor_field,
                                tipo_field,
                                modo_field,
                                pago_field,
                                observacao_field,
                                local_field,
                                dt_vencimento_field,
                                ft.Row([
                                    ft.ElevatedButton(text="Salvar Alterações", icon=ft.Icons.SAVE, bgcolor="#44CFA1",
                                                      color="white", on_click=salvar_click),
                                    ft.ElevatedButton(text="Excluir Transação", icon=ft.Icons.DELETE, bgcolor="#F28B82",
                                                      color="white", on_click=excluir_click),
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
