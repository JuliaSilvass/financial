import flet as ft
from services.session_manager import SessionManager
from controllers.transacao_controller import TransacaoController
from controllers.ambiente_controller import AmbienteController
from controllers.categoria_controller import CategoriaController
from controllers.conta_controller import ContaController
from utils.sidebar import build_sidebar
from utils.dialogs import show_confirm_dialog, show_alert
from utils.list_page import build_list_page
from utils.search_bar import build_search_bar
from utils.replace import to_float
from utils.date import date_picker_br

# ==========================================================
# Sidebar 
# ==========================================================
def transacao_sidebar(page, user, active_route: str):
    menu_items = [
        {"label": "Listar Transações", "route": "/transacao/listar", "icon": ft.Icons.LIST},
        {"label": "Cadastrar Nova", "route": "/transacao/cadastrar", "icon": ft.Icons.ADD},
    ]
    return build_sidebar(
        page=page,
        user=user,
        menu_items=menu_items,
        active_route=active_route
    )


# ==========================================================
# LISTAR TRANSAÇÕES
# ==========================================================
def transacao_listar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/transacao/listar", controls=[])

    user = SessionManager.get_current_user()
    controller = TransacaoController()

    sidebar = transacao_sidebar(page, user, "/transacao/listar")

    transacoes = controller.listar_transacoes(user["id"])
    columns = [
        {
            "label": "Transação", 
            "field": "transacao_descricao",
            "width": 200
         },
    ]

    def on_click(tra):
        page.go(f"/transacao/detalhar/{tra.transacao_id}")

    # --------------------------------------------------
    # Tabela (variável que será atualizada)
    # --------------------------------------------------
    tabela = build_list_page(
        items=transacoes,
        columns=columns,
        on_item_click=on_click,
    )   

    # --------------------------------------------------
    # Busca
    # --------------------------------------------------
    def on_search(texto):
        texto = texto.lower()

        filtrados = [
            tra for tra in transacoes
            if texto in tra.transacao_nome.lower()
            or (tra.transacao_descricao and texto in tra.transacao_descricao.lower())
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
        hint_text="Pesquisar transações...",
        on_change=on_search,
    ) 

    # --------------------------------------------------
    # Recria tabela com search bar
    # --------------------------------------------------
    tabela = build_list_page(
        items=transacoes,
        columns=columns,
        on_item_click=on_click,
        search_bar=search_bar,
    )   

    def voltar_click(e):
        page.go("/dashboard")

    return ft.View(
        route="/transacao/listar",
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
                                            "Transações Cadastradas", 
                                            size=26, 
                                            weight="bold", 
                                        )
                                    ]
                                ),
                                ft.Divider(),
                                tabela
                            ],
                        ),
                    )
                ],
            )
        ],
    )


# ==========================================================
# CADASTRAR TRANSAÇÃO
# ==========================================================
def transacao_cadastrar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/transacao/cadastrar", controls=[])

    user = SessionManager.get_current_user()
    transacaoController = TransacaoController()
    ambienteController = AmbienteController()
    categoriaController = CategoriaController()
    contaController = ContaController()
    # metaController = MetaController()

    sidebar = transacao_sidebar(page, user, "/transacao/cadastrar")

    ambientes = ambienteController.listar_ambientes(user["id"])
    categorias = categoriaController.listar_categoria(user["id"])
    contas = contaController.listar_conta(user["id"])
    # metas = metaController.listar_meta(user["id"])

    contas_map = {
        str(ct.conta_id): ct.conta_tipo
        for ct in contas
    }

    def on_conta_change(e):
        conta_id = e.control.value

        if not conta_id:
            cartao_credito_container.visible = False
            page.update()
            return

        tipo_conta = contas_map.get(conta_id)

        if tipo_conta == "Cartão de Crédito":
            cartao_credito_container.visible = True
        else:
            cartao_credito_container.visible = False

        page.update()

    def on_recorrente_change(e):
        if recorrente_field.value:
            recorrencia_container.visible = True
        else:
            recorrencia_container.visible = False
            dt_fim_recorrencia_field_container.visible = False
        page.update()

    def on_recorrencia_fim(e):
        if tipoRecorrencia_field.value == "fixa":
            dt_fim_recorrencia_field_container.visible = False
        else:
            dt_fim_recorrencia_field_container.visible = True
        page.update()


    # Campos principais
    descricao_field = ft.TextField(
        label="Descrição da transação", 
        width=400,
        hint_text="Ex: Compra no supermercado"
        )
    
    valor_field = ft.TextField(
        label="Valor (R$)", 
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9.,]"),
        hint_text="Ex: 1500,00",
        )
    
    data_field, date_picker = date_picker_br(
        page,
        label="Data da Transação"
    )

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

    local_field = ft.TextField(
        label="Local (opcional)",
        width=400,
        hint_text="Ex: Supermercado XYZ"
    )

    observacao_field = ft.TextField(
        label="Observação (opcional)",
        width=400,
        hint_text="Ex: Compra realizada com desconto"
    )

    recorrente_field = ft.Checkbox(
        label="Recorrente", 
        value=False,
        on_change=on_recorrente_change
    )

    frequencia_field = ft.Dropdown(
        label="Frequência (se recorrente)",
        width=400,
        options=[
            ft.dropdown.Option("diaria", "Diária"),
            ft.dropdown.Option("semanal", "Semanal"),
            ft.dropdown.Option("mensal", "Mensal"),
            ft.dropdown.Option("anual", "Anual"),
        ]
    )
    
    tipoRecorrencia_field = ft.Dropdown(
        label="Tipo de Recorrência (se recorrente)",
        width=400,
        options=[
            ft.dropdown.Option("fixa", "Fixa"),
            ft.dropdown.Option("variavel", "Variável"),
        ],
        on_change=on_recorrencia_fim
    )

    dt_fim_recorrencia_field, date_picker_fim_recorrencia = date_picker_br(
        page,
        label="Data de Fim da Recorrência (Opcional)"
    )

    # meta_field = ft.Dropdown(
    #     label="Meta (opcional)",
    #     width=400,
    #     options=[ft.dropdown.Option(str(m.meta_id), m.meta_nome) for m in []],  # metas
    # )

    conta_field = ft.Dropdown(
        label="Conta",
        width=400,
        options=[ft.dropdown.Option(str(ct.conta_id), ct.conta_nome) for ct in contas],
        on_change=on_conta_change
    )

    dt_pagamento_field, date_picker_pag = date_picker_br(
        page,
        label="Data do pagamento (Opcional)"
    )

    dt_vencimento_field, date_picker_venc = date_picker_br(
        page,
        label="Data do vencimento (Opcional)"
    )

    # Mudar isso pra um tipo de seletor...
    total_parcelas_field = ft.TextField(
        label="Total de parcelas (se parcelado)",
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9]"),
        hint_text="Ex: 12"
    )

    parcela_atual_field = ft.TextField(
        label="Parcela atual (se parcelado)",
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9]"),
        hint_text="Ex: 1"
    )

    pago_field = ft.Checkbox(
        label="Pago", 
        value=False,
    )

    mensagem = ft.Text(color="green")


    def to_float(value):
        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return 0.0

    def voltar_click(e):
        page.go("/transacao/listar")


    cartao_credito_container = ft.Column(
        controls=[
            total_parcelas_field,
            parcela_atual_field,
            dt_vencimento_field,
        ],
        visible=False,
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    recorrencia_container = ft.Column(
        controls=[
            tipoRecorrencia_field,
            frequencia_field,
        ],
        visible=False,
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    dt_fim_recorrencia_field_container = ft.Column(
        controls=[
            dt_fim_recorrencia_field
        ],
        visible=False,
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def salvar_click(e):
        descricao = descricao_field.value.strip()
        valor = to_float(valor_field.value)
        data = date_picker.value.strip()
        ambiente_id = ambiente_field.value
        categoria_id = categoria_field.value
        # meta_id = meta_field.value if meta_field.value else None
        local = local_field.value.strip()
        observacao = observacao_field.value.strip()
        recorrencia = recorrente_field.value
        frequencia = frequencia_field.value
        tipoRecorrencia = tipoRecorrencia_field.value
        dt_fim_recorrencia = date_picker_fim_recorrencia.value.strip()
        modo = modo_field.value     
        tipo = tipo_field.value
        pago = pago_field.value
        data_pagamento = date_picker_pag.value.strip()
        data_vencimento = date_picker_venc.value.strip()
        total_parcelas = total_parcelas_field.value.strip()
        parcela_atual = parcela_atual_field.value.strip()
        conta_id = conta_field.value

        # TODO: PRECISA AJUSTAR ESSA VALIDAÇÃO... PARA CADA CAMPO
        if not conta_id or not descricao or not data or valor <= 0 or not tipo or not modo or not ambiente_id or not categoria_id:
            show_alert(
                page, 
                "Campo obrigatório",
                f"O campo {conta_field.label} é obrigatório para cadastrar uma transação."
            )
            return

        ok, msg = transacaoController.register_transacao(
            descricao=descricao,
            valor=valor,
            data=data,
            ambiente_id=int(ambiente_id),
            categoria_id=int(categoria_id),
            # meta_id=int(meta_id),
            local=local,
            observacao=observacao,
            recorrencia=recorrencia,
            frequencia=frequencia,
            tipo_recorrencia=tipoRecorrencia,
            dt_fim_recorrencia=dt_fim_recorrencia,
            modo=modo,
            tipo=tipo,
            pago=pago,
            dt_pagamento=data_pagamento,
            dt_vencimento=data_vencimento,
            total_parcelas=total_parcelas,
            parcela_atual=parcela_atual, 
            conta_id=int(conta_id)
        )


        if ok:
            # descricao_field.value = ""
            # valor_field.value = ""
            # data_field.value = ""
            # tipo_field.value = None
            # modo_field.value = None
            # ambiente_field.value = ""
            # categoria_field.value = ""
            # conta_field.value = ""
            # pago_field.value = True

            page.go("/transacao/listar")
        else :
            show_alert(
                page,
                "Erro ao salvar", msg
            )

        page.update()

    return ft.View(
        route="/transacao/cadastrar",
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
                            expand=True,
                            spacing=20,
                            controls=[
                                # ------------------------
                                # CABEÇALHO (FIXO)
                                # ------------------------
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            tooltip="Voltar",
                                            on_click=voltar_click
                                        ),
                                        ft.Text(
                                            "Cadastrar Nova Transação",
                                            size=26,
                                            weight="bold"
                                        )
                                    ]
                                ),
                                ft.Divider(),

                                # ------------------------
                                # COM SCROLL
                                # ------------------------
                                ft.Container(
                                    expand=True,
                                    content=ft.Column(
                                        expand=True,
                                        scroll=ft.ScrollMode.AUTO, 
                                        spacing=20,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            descricao_field,
                                            local_field,
                                            valor_field,
                                            data_field,
                                            tipo_field,
                                            ft.Container(
                                                width=400,
                                                alignment=ft.alignment.center_left,
                                                content=recorrente_field
                                            ),
                                            recorrencia_container,
                                            dt_fim_recorrencia_field_container,
                                            modo_field,
                                            ambiente_field,
                                            categoria_field,
                                            conta_field,
                                            cartao_credito_container,
                                            ft.Container(
                                                width=400,
                                                alignment=ft.alignment.center_left,
                                                content=pago_field
                                            ),
                                            dt_pagamento_field,
                                            observacao_field,
                                            ft.ElevatedButton(
                                                text="Salvar Transação",
                                                icon=ft.Icons.SAVE,
                                                bgcolor="#44CFA1",
                                                color="white",
                                                on_click=salvar_click
                                            ),
                                            mensagem
                                        ],
                                    ),
                                )
                            ],
                        )

                    )
                ],
            )
        ],
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
                    transacao_sidebar(user, page, "/transacao/detalhar"),
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
