import flet as ft

def home_page(page: ft.Page):
    page.clean()

    def login_click(e):
        page.go("/login")

    def register_click(e):
        page.go("/register")

        # Botão de Login (principal)
    btn_login = ft.ElevatedButton(
        text="Login",
        icon=ft.Icons.LOGIN,
        style=ft.ButtonStyle(
            bgcolor={"":"#44CFA1"},
            color={"":"white"},
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=login_click
    )

    # Botão de Registrar (alternativo)
    btn_register = ft.ElevatedButton(
        text="Registrar",
        icon=ft.Icons.APP_REGISTRATION,
        style=ft.ButtonStyle(
            bgcolor={"":"#44CFA1"},
            color={"":"white"},
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
            side={"":ft.BorderSide(2, "#44CFA1")} 
        ),
        on_click=register_click
    )

    return ft.View(
        route="/", 
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Bem vindo ao Financial!", theme_style="displayMedium", size=50, weight="bold", color="#44CFA1", no_wrap=False),
                    ft.Text("Aqui você pode gerenciar sua vida financeira e acompanhar o andamento de suas finanças.", size=25, no_wrap=False),
                    ft.Divider(),
                    ft.Text("Para começar, faça login ou registre-se.", size=25),
                    ft.Row(
                        controls=[btn_login, btn_register],
                        alignment="center"
                    )
                ],
                alignment="center",
                horizontal_alignment="center",
                expand=True
            )
        ],
        horizontal_alignment="center",
        vertical_alignment="center"
    )