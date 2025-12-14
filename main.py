import flet as ft
from ui.home_page import home_page
from ui.login_page import login_page
from ui.register_page import register_page
from ui.dashboard_page import dashboard_page
from ui.ambiente_page import (
    ambiente_cadastrar_page,
    ambiente_listar_page,
    ambiente_detalhar_page,
)
from ui.categoria_page import (
    categoria_listar_page, 
    categoria_cadastrar_page,
    categoria_detalhar_page
)
from ui.conta_page import (
    conta_listar_page, 
    conta_cadastrar_page,
    conta_detalhar_page
)
from ui.transacoes_page import (
    transacao_listar_page, 
    transacao_cadastrar_page,
    transacao_detalhar_page
)
from database.connection_db import test_connection


# -------------------------------------------------------------
# Função principal
# -------------------------------------------------------------
def main(page: ft.Page):
    page.title = "Financial"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Testa conexão com o banco (só na inicialização)
    test_connection()

    # ---------------------------------------------------------
    # Sistema de Rotas
    # ---------------------------------------------------------
    def route_change(e: ft.RouteChangeEvent):
        route = page.route
        page.views.clear()

        # Rota dinâmica: /ambiente/detalhar/{id}
        if route.startswith("/ambiente/detalhar/"):
            try:
                ambiente_id = int(route.split("/")[-1])
                page.views.append(ambiente_detalhar_page(page, ambiente_id))
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("ID inválido para ambiente."))
                page.snack_bar.open = True
                page.go("/ambiente/listar")
            page.update()
            return  # evita cair no dicionário abaixo
        
        # Rota dinâmica: /categoria/detalhar/{id}
        if route.startswith("/categoria/detalhar/"):
            try:
                categoria_id = int(route.split("/")[-1])
                page.views.append(categoria_detalhar_page(page, categoria_id))
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("ID inválido para categoria."))
                page.snack_bar.open = True
                page.go("/categoria/listar")
            page.update()
            return  

        # Rota dinâmica: /conta/detalhar/{id}
        if route.startswith("/conta/detalhar/"):
            try:
                conta_id = int(route.split("/")[-1])
                page.views.append(conta_detalhar_page(page, conta_id))
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("ID inválido para conta."))
                page.snack_bar.open = True
                page.go("/conta/listar")
            page.update()
            return
        
        # Rota dinâmica: /transacao/detalhar/{id}
        # Rota dinâmica: /transacao/detalhar/{id}
        if route.startswith("/transacao/detalhar/"):
            try:
                transacao_id = int(route.split("/")[-1])
                page.views.append(transacao_detalhar_page(page, transacao_id))
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("ID inválido para transação."))
                page.snack_bar.open = True
                page.go("/transacao/listar")
            page.update()
            return


        # Demais rotas fixas
        routes = {
            "/": home_page,
            "/login": login_page,
            "/register": register_page,
            "/dashboard": dashboard_page,
            "/ambiente/cadastrar": ambiente_cadastrar_page,
            "/ambiente/listar": ambiente_listar_page,
            "/categoria/cadastrar": categoria_cadastrar_page,
            "/categoria/listar": categoria_listar_page,
            "/conta/cadastrar": conta_cadastrar_page,
            "/conta/listar": conta_listar_page,
            "/transacao/cadastrar": transacao_cadastrar_page,
            "/transacao/listar": transacao_listar_page,
        }

        # Se a rota existir, renderiza a página correspondente
        if route in routes:
            page.views.append(routes[route](page))
        else:
            page.views.append(home_page(page))  # rota padrão (fallback)

        page.update()
    # Define o callback e abre a página inicial
    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
