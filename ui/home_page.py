import flet as ft

def home_page(page: ft.Page):
    page.clean()

    def login_click(e):
        print("Clicou em login")

    def register_click(e):
        print("Clicou em registrar")

    btn_login = ft.ElevatedButton("Login", on_click=login_click)
    btn_register = ft.ElevatedButton("Registrar", on_click=register_click)
    
    page.add(
        ft.Row(
            [
                ft.Text("Bem-vindo ao financial!", size=40, weight="bold", color="Green"),
                ft.Text("Aqui você pode gerenciar sua vida financeira, e acompanhar o andamento de suas finanças.", size=16),
                ft.Text("Para começar, faça login ou registre-se.", size=16),
            ],
            alignment="center"
        ),
        btn_login,
        btn_register
    )
