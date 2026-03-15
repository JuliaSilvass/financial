from datetime import datetime

import flet as ft
from services.session_manager import SessionManager
from controllers.meta_controller import MetaController
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
def meta_sidebar(page, user, active_route: str):
    menu_items = [
        {"label": "Listar Metas", "route": "/meta/listar", "icon": ft.Icons.LIST},
        {"label": "Cadastrar Nova", "route": "/meta/cadastrar", "icon": ft.Icons.ADD},
    ]
    return build_sidebar(
        page=page,
        user=user,
        menu_items=menu_items,
        active_route=active_route
    )


# ==========================================================
# LISTAR METAS
# ==========================================================
def meta_listar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/meta/listar", controls=[])

    user = SessionManager.get_current_user()
    controller = MetaController()

    sidebar = meta_sidebar(page, user, "/meta/listar")
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    metas = controller.listar_metas(user["id"])
    for meta in metas:
        meta.meta_nome = meta.meta_nome if meta.meta_nome else "-"

    columns = [
        {
            "label": "Meta", 
            "field": "meta_nome",
            "width": 200
        },
        {
            "label": "Descrição", 
            "field": "meta_descricao",
            "width": 200
        },
        {
            "label": "Data Inicio",
            "field": "meta_dt_inicial",
            "width": 150,
            "type": "date"    
        },
        {
            "label": "Data Alvo", 
            "field": "meta_dt_limite",
            "width": 150,
            "type": "date"    
        },
        {
            "label": "Valor Alvo (R$)", 
            "field": "meta_valor_alvo",
            "width": 150,
        },
        {
            "label": "Valor Atual (R$)", 
            "field": "meta_valor_atual",
            "width": 150,
        },
        # {
        #     "label": "Progresso", 
        #     "field": "meta_concluida",
        #     "width": 150,
        # },
        {
            "label": "Status", 
            "field": "meta_concluida",
            "width": 150
        }
    ]

    def on_click(meta):
        page.go(f"/meta/detalhar/{meta.meta_id}")

    # --------------------------------------------------
    # Tabela (variável que será atualizada)
    # --------------------------------------------------
    tabela = build_list_page(
        items=metas,
        columns=columns,
        on_item_click=on_click,
    )   

    # --------------------------------------------------
    # Busca
    # --------------------------------------------------
    def on_search(texto):
        texto = texto.lower()

        filtrados = [
            meta for meta in metas
            if texto in meta.meta_nome.lower()
            or (meta.meta_descricao and texto in meta.meta_descricao.lower())
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
        hint_text="Pesquisar metas...",
        on_change=on_search,
    ) 

    # --------------------------------------------------
    # Recria tabela com search bar
    # --------------------------------------------------
    tabela = build_list_page(
        items=metas,
        columns=columns,
        on_item_click=on_click,
        search_bar=search_bar,
    )   

    def voltar_click(e):
        page.go("/dashboard")

    return ft.View(
        route="/meta/listar",
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
                                            "Metas Cadastradas", 
                                            size=26, 
                                            weight="bold", 
                                        ),
                                    ],
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
# CADASTRAR META
# ==========================================================
def meta_cadastrar_page(page: ft.Page):
    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route="/meta/cadastrar", controls=[])

    user = SessionManager.get_current_user()
    ambienteController = AmbienteController()
    # categoriaController = CategoriaController()
    contaController = ContaController()
    metaController = MetaController()

    sidebar = meta_sidebar(page, user, "/meta/cadastrar")

    ambientes = ambienteController.listar_ambientes(user["id"])
    # categorias = categoriaController.listar_categoria(user["id"])
    contas = contaController.listar_conta(user["id"])
    metas = metaController.listar_metas(user["id"])

    # contas_map = {
    #     str(ct.conta_id): ct
    #     for ct in contas
    # }

    # def on_conta_change(e):
    #     conta_id = e.control.value

    #     if not conta_id:
    #         cartao_credito_container.visible = False
    #         page.update()
    #         return

    #     conta = contas_map.get(conta_id)

    #     if not conta:
    #         return

    #     if conta.conta_tipo == "Cartão de Crédito":
    #         cartao_credito_container.visible = True

    #         if conta.conta_dia_vencimento:
    #             hoje = datetime.now()
    #             ano = hoje.year
    #             mes = hoje.month

    #             try:
    #                 data_venc = datetime(ano, mes, int(conta.conta_dia_vencimento))
    #             except ValueError:
    #                 from calendar import monthrange
    #                 ultimo_dia = monthrange(ano, mes)[1]
    #                 data_venc = datetime(ano, mes, ultimo_dia)

    #             date_picker_venc.value = data_venc.strftime("%d/%m/%Y")

    #     else:
    #         cartao_credito_container.visible = False
    #         date_picker_venc.value = ""

    #     page.update()

    # Campos principais
    meta_nome = ft.TextField(
        label="Nome da meta", 
        width=400,
        hint_text="Ex: Compra um carro novo"
        )
    
    meta_descricao = ft.TextField(
        label="Descrição da meta", 
        width=400,
        hint_text="Ex: Quero juntar dinheiro para comprar um carro novo em 2 anos."
        )
    
    meta_valor_alvo = ft.TextField(
        label="Valor alvo (R$)", 
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9.,]"),
        hint_text="Ex: 150000,00",
        )
    
    meta_valor_atual = ft.TextField(
        label="Valor atual (R$)", 
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9.,]"),
        hint_text="Ex: 150000,00",
        )
    
    data_inicio, date_inicio_picker = date_picker_br(
        page,
        label="Data da inicio",
    )

    data_fim, date_fim_picker = date_picker_br(
        page,
        label="Data do fim",
    )
    
    meta_estado = ft.Switch(
        label="Meta concluída",
        value=False
    )

    ambiente_field = ft.Dropdown(
        label="Ambiente",
        width=400,
        options=[ft.dropdown.Option(str(a.ambiente_id), a.ambiente_nome) for a in ambientes],
    )

    # categoria_field = ft.Dropdown(
    #     label="Categoria",
    #     width=400,
    #     options=[ft.dropdown.Option(str(c.categoria_id), c.categoria_nome) for c in categorias],
    # )

    # conta_field = ft.Dropdown(
    #     label="Conta",
    #     width=400,
    #     options=[ft.dropdown.Option(str(ct.conta_id), ct.conta_nome) for ct in contas],
    #     on_change=on_conta_change
    # )

    mensagem = ft.Text()


    def to_float(value):
        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return 0.0

    def voltar_click(e):
        page.go("/meta/listar")


    # cartao_credito_container = ft.Column(
    #     controls=[
    #     ],
    #     visible=False,
    #     spacing=20,
    #     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    # )


    def salvar_click(e):
        nome = meta_nome.value.strip()
        descricao = meta_descricao.value.strip()
        valor_alvo = to_float(meta_valor_alvo.value)
        valor_atual = to_float(meta_valor_atual.value)
        data_inicio = datetime.strptime(date_inicio_picker.value, "%d/%m/%Y").date()
        data_fim = datetime.strptime(date_fim_picker.value, "%d/%m/%Y").date()
        status = meta_estado.value
        ambiente_id = ambiente_field.value
        # categoria_id = categoria_field.value
        # conta_id = conta_field.ft.Container(

        campos = {
            "Nome da meta": nome,
            "Descrição": descricao,
            "Data de início": data_inicio,
            "Data de fim": data_fim,
            "Ambiente": ambiente_id
        }

        for nome_campo, valor in campos.items():
            if not valor:
                show_alert(
                    page,
                    "Campo obrigatório",
                    f"O campo '{nome_campo}' é obrigatório."
                )
                return

        if valor_alvo <= 0:
            show_alert(
                page,
                "Campo obrigatório",
                "O valor alvo deve ser maior que zero."
            )
            return

        ok, msg = metaController.register_meta(
            nome=nome,
            descricao=descricao,
            valor_alvo=valor_alvo,
            valor_atual=valor_atual,
            data_inicio=data_inicio,
            data_fim=data_fim,
            status=status,
            ambiente_id=int(ambiente_id),
            usuario_id=int(user["id"]),
            # categoria_id=int(categoria_id),
            # conta_id=int(conta_id)
        )


        if ok:
            meta_descricao.value = ""
            meta_valor_alvo.value = ""
            meta_valor_atual.value = ""
            date_inicio_picker.value = ""
            date_fim_picker.value = ""
            ambiente_field.value = ""
            # categoria_field.value = ""
            # conta_field.value = ""

            page.go("/meta/listar")
        else :
            show_alert(
                page,
                "Erro ao salvar", msg
            )

        page.update()

    return ft.View(
        route="/meta/cadastrar",
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
                                            "Cadastrar Nova Meta",
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
                                            meta_nome,
                                            meta_descricao,
                                            meta_valor_alvo,
                                            meta_valor_atual,
                                            data_inicio,
                                            data_fim,
                                            ambiente_field,
                                            # categoria_field,
                                            # conta_field,
                                            ft.ElevatedButton(
                                                text="Salvar Meta",
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


# # --------------------------------------------------------------------
# # Página de DETALHES / EDIÇÃO / EXCLUSÃO
# # --------------------------------------------------------------------
def meta_detalhar_page(page: ft.Page, meta_id: int):

    if not SessionManager.is_logged_in():
        page.go("/login")
        return ft.View(route=f"/meta/detalhar/{meta_id}", controls=[])

    user = SessionManager.get_current_user()

    ambienteController = AmbienteController()
    categoriaController = CategoriaController()
    contaController = ContaController()
    metaController = MetaController()

    ambientes = ambienteController.listar_ambientes(user["id"])
    categorias = categoriaController.listar_categoria(user["id"])
    contas = contaController.listar_conta(user["id"])
    meta = metaController.get_meta(meta_id)

    if not meta:
        show_alert(
            page, 
            "Meta não encontrada",
            "A meta que você está tentando acessar não existe ou foi removida."    
        )
        page.go("/meta/listar")
        return

    sidebar = meta_sidebar(page, user, "/meta/detalhar")

    # --- Campos editáveis ---

#     contas_map = {
#         str(ct.conta_id): ct
#         for ct in contas
#     }

#     def on_conta_change(e):
#         conta_id = e.control.value

#         if not conta_id:
#             cartao_credito_container.visible = False
#             page.update()
#             return

#         conta = contas_map.get(conta_id)

#         if not conta:
#             return

#         if conta.conta_tipo == "Cartão de Crédito":
#             cartao_credito_container.visible = True

#             if conta.conta_dia_vencimento:
#                 hoje = datetime.now()
#                 ano = hoje.year
#                 mes = hoje.month

#                 try:
#                     data_venc = datetime(ano, mes, int(conta.conta_dia_vencimento))
#                 except ValueError:
#                     from calendar import monthrange
#                     ultimo_dia = monthrange(ano, mes)[1]
#                     data_venc = datetime(ano, mes, ultimo_dia)

#                 date_picker_venc.value = data_venc.strftime("%d/%m/%Y")

#         else:
#             cartao_credito_container.visible = False
#             date_picker_venc.value = ""

#         page.update()


    meta_nome = ft.TextField(
            label="Nome da meta", 
            width=400,
            hint_text="Ex: Comprar um carro novo",
            value=meta.meta_nome
            )
    meta_descricao = ft.TextField(
            label="Descrição da meta",
            width=400,
            hint_text="Ex: Quero juntar dinheiro para comprar um carro novo em 2 anos.",
            value=meta.meta_descricao
            )
    
    meta_valor_alvo = ft.TextField(
        label="Valor alvo (R$)", 
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9.,]"),
        hint_text="Ex: 150000,00",
        value=meta.meta_valor_alvo
        )
    
    
    meta_valor_atual = ft.TextField(
        label="Valor atual (R$)", 
        width=400,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(r"[0-9.,]"),
        hint_text="Ex: 150000,00",
        value=meta.meta_valor_atual
    )

    data_inicio, date_inicio_picker = date_picker_br(
        page,
        label="Data de inicio",
        value=meta.meta_dt_inicial
    )

    data_fim, date_fim_picker = date_picker_br(
        page,
        label="Data de fim",
        value=meta.meta_dt_limite
    )

    meta_estado = ft.Switch(
        label="Meta concluída",
        value=meta.meta_concluida
    )

    ambiente_field = ft.Dropdown(
        label="Ambiente",
        width=400,
        options=[ft.dropdown.Option(str(a.ambiente_id), a.ambiente_nome) for a in ambientes],
        value=str(meta.ambiente_id) if meta.ambiente_id else None
    )

    mensagem = ft.Text()

    def voltar_click(e):
        page.go("/meta/listar")

    # --- SALVAR ALTERAÇÕES ---
    def salvar_click(e):
        nome = meta_nome.value.strip()
        descricao = meta_descricao.value.strip()
        valor_alvo = to_float(meta_valor_alvo.value)
        valor_atual = to_float(meta_valor_atual.value)
        data_inicio = datetime.strptime(date_inicio_picker.value, "%d/%m/%Y").date()
        data_fim = datetime.strptime(date_fim_picker.value, "%d/%m/%Y").date()
        status = meta_estado.value
        ambiente_id = ambiente_field.value
        # categoria_id = categoria_field.value

        campos = {
            "Nome da meta": nome,
            "Descrição": descricao,
            "Data de início": data_inicio,
            "Data de fim": data_fim,
            "Ambiente": ambiente_id
        }

        for nome_campo, valor in campos.items():
            if not valor:
                show_alert(
                    page,
                    "Campo obrigatório",
                    f"O campo '{nome_campo}' é obrigatório."
                )
                return

        if valor_alvo <= 0:
            show_alert(
                page,
                "Campo obrigatório",
                "O valor alvo deve ser maior que zero."
            )
            return

        ok, msg = metaController.update_meta(
            meta_id=meta_id,
            nome=nome,
            descricao=descricao,
            valor_alvo=valor_alvo,
            valor_atual=valor_atual,
            data_inicio=data_inicio,
            data_fim=data_fim,
            status=status,
            ambiente_id=int(ambiente_id),
            # categoria_id=int(categoria_id)
        )

        if ok:
            show_alert(page, "Sucesso", msg)
        else :
            show_alert(page, "Erro", msg)

    # --- EXCLUIR META ---
    def excluir_click(e):
        def confirmar_excluir():
            ok, msg = metaController.delete_meta(meta_id)
            if ok:
                page.go("/meta/listar")
            else:
                show_alert(page, "Erro", msg)

        show_confirm_dialog(
            page,
            title="Confirmar Exclusão",
            message="Tem certeza que deseja excluir esta meta? Esta ação é irreversível.",
            on_confirm=confirmar_excluir
            )
    
    # --- VIEW FINAL ---
    return ft.View(
        route=f"/meta/detalhar/{meta_id}",
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
                                            "Cadastrar Nova Meta",
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
                                            meta_nome,
                                            meta_descricao, 
                                            meta_valor_alvo,
                                            meta_valor_atual,
                                            data_inicio,
                                            data_fim,
                                            ambiente_field,
                                            ft.Row(
                                                [
                                                    ft.ElevatedButton(
                                                        text="Salvar Alterações",
                                                        icon=ft.Icons.SAVE,
                                                        bgcolor="#44CFA1",
                                                        color="white",
                                                        on_click=salvar_click
                                                    ),
                                                    ft.OutlinedButton(
                                                        "Excluir Transação",
                                                        icon=ft.Icons.DELETE,
                                                        on_click=excluir_click,
                                                    ),
                                                ],
                                                spacing=15,
                                                alignment=ft.MainAxisAlignment.CENTER,
                                            ),
                                            mensagem
                                        ],
                                    ),
                                )
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )
