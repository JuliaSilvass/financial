import flet as ft
from controllers.user_controller import UserController
from utils.dialogs import show_alert
from utils.security import validate_password


def register_page(page: ft.Page):

    check_length = ft.Text("• Mínimo 8 caracteres", color="red")
    check_upper = ft.Text("• Letra maiúscula", color="red")
    check_lower = ft.Text("• Letra minúscula", color="red")
    check_number = ft.Text("• Número", color="red")
    check_special = ft.Text("• Caractere especial", color="red")
    check_match = ft.Text("• Senhas coincidem", color="red")

    controller = UserController()

    def update_password_checks(password: str):
        rules = validate_password(password)

        check_length.color = "green" if rules["length"] else "red"
        check_upper.color = "green" if rules["upper"] else "red"
        check_lower.color = "green" if rules["lower"] else "red"
        check_number.color = "green" if rules["number"] else "red"
        check_special.color = "green" if rules["special"] else "red"

        page.update()
    
    def check_password_match(e=None):
        if txt_pass.value and txt_pass.value == txt_pass_confirm.value:
            check_match.color = "green"
        else:
            check_match.color = "red"
        page.update()

    # Campos de cadastro
    txt_user = ft.TextField(label="Nome", width=300)
    txt_email = ft.TextField(label="Email", width=300)
    txt_pass = ft.TextField(
        label="Senha",
        password=True,
        width=300,
        on_change=lambda e: update_password_checks(e.control.value),
    )
    txt_pass_confirm = ft.TextField(
        label="Confirmar Senha",
        password=True,
        width=300,
        on_change=check_password_match,
    )
    password_rules_box = ft.Container(
        content=ft.Column(
            controls=[
                check_length,
                check_upper,
                check_lower,
                check_number,
                check_special,
                check_match,
            ],
            spacing=4,
        ),
        padding=10,
        border_radius=8,
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
        width=300,
    )

    # Função do botão de registrar
    def register_click(e):
        user = txt_user.value.strip()
        email = txt_email.value.strip()
        password = txt_pass.value
        password_confirm = txt_pass_confirm.value

        if password != password_confirm:
            show_alert(page, "Erro", "As senhas não coincidem.")
            return

        success, message = controller.register_user(user, email, password)

        show_alert(
            page,
            "Sucesso" if success else "Erro",
            message
        )

        if success:
            txt_user.value = ""
            txt_email.value = ""
            txt_pass.value = ""
            txt_pass_confirm.value = ""
            page.update()

    #Função do botão de voltar para home
    def backToHome_click(e):
        page.go("/")
    

    # Botão de registrar
    btn_register = ft.ElevatedButton(
        text="Registrar",
        style=ft.ButtonStyle(
            bgcolor={"": "#44CFA1"},
            color={"": "white"},
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=register_click
    )

    # Botão de Voltar para Home
    btn_backToHome = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="white",
        bgcolor="#44CFA1",
        on_click=backToHome_click
    )


    # Retornar a View com os controles
    return ft.View(
        route="/register",
        controls=[
            ft.Column(
                controls=[  
                    ft.Text("Registrar-se", theme_style="displayMedium", size=40, weight="bold", color="#44CFA1"),
                    ft.Text("Preencha os campos abaixo para criar uma nova conta.", size=20),
                        txt_user, 
                        txt_email, 
                        txt_pass,
                        password_rules_box,
                        txt_pass_confirm,
                        btn_register,
                        btn_backToHome],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        ],
        horizontal_alignment="center",
        vertical_alignment="center"
    )


