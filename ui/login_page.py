import flet as ft
from controllers.user_controller import UserController
from utils.dialogs import show_alert

def login_page(page: ft.Page):

    controller = UserController()

    email_ok = False
    password_ok = False
    txt_email = None
    txt_pass = None


    def update_login_button_state():
        nonlocal email_ok, password_ok

        if txt_email is None or txt_pass is None:
            return

        btn_login.disabled = not (email_ok and password_ok)
        page.update()

    def on_email_change(e):
        nonlocal email_ok
        email_ok = bool((txt_email.value or "").strip())
        update_login_button_state()

    def on_password_change(e):
        nonlocal password_ok
        password_ok = bool((txt_pass.value or "").strip())
        update_login_button_state()

    def login_click(e):
        email = (txt_email.value or "").strip()
        password = (txt_pass.value or "").strip()

        if not email or not password:
            show_alert(page, "Erro", "Email ou senha inválidos.")
            return

        success, _ = controller.login_user(email, password)

        if not success:
            show_alert(page, "Erro", "Email ou senha inválidos.")
            return

        page.go("/dashboard")

    def backToHome_click(e):
        page.go("/")


    btn_login = ft.ElevatedButton(
        text="Login",
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor={"": "#44CFA1", "disabled": "#BFE9DA"},
            color={"": "white", "disabled": "#EEEEEE"},
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=login_click,
    )

    btn_backToHome = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="white",
        bgcolor="#44CFA1",
        on_click=backToHome_click,
    )

    txt_email = ft.TextField(
        label="Email",
        width=300,
        on_change=on_email_change,
    )

    txt_pass = ft.TextField(
        label="Senha",
        password=True,
        width=300,
        on_change=on_password_change,
        on_submit=login_click, 
    )

    update_login_button_state()

    return ft.View(
        route="/login",
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Login", theme_style="displayMedium", size=40, weight="bold", color="#44CFA1"),
                    ft.Text("Preencha os campos abaixo para logar na conta", size=20),
                    txt_email,
                    txt_pass,
                    btn_login,
                    btn_backToHome,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        ],
        horizontal_alignment="center",
        vertical_alignment="center",
    )
