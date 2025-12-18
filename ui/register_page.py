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

    password_valid = False
    passwords_match = False
    password_focus_count = 0


    controller = UserController()

    def on_password_focus(e):
        nonlocal password_focus_count
        password_focus_count += 1
        password_rules_box.visible = True
        page.update()

    def on_password_blur(e):
        nonlocal password_focus_count
        password_focus_count -= 1

        if password_focus_count <= 0:
            password_rules_box.visible = False
            password_focus_count = 0

        page.update()


    def show_password_rules(e):
        password_rules_box.visible = True
        page.update()

    def hide_password_rules(e):
        password_rules_box.visible = False
        page.update()

    def update_register_button_state():
        nonlocal password_valid, passwords_match

        name_ok = txt_user.value and len(txt_user.value.strip()) >= 3
        email_ok = txt_email.value and "@" in txt_email.value

        btn_register.disabled = not (
            name_ok and email_ok and password_valid and passwords_match
        )

        page.update()


    def update_password_checks(password: str):
        nonlocal password_valid

        rules = validate_password(password)

        check_length.color = "green" if rules["length"] else "red"
        check_upper.color = "green" if rules["upper"] else "red"
        check_lower.color = "green" if rules["lower"] else "red"
        check_number.color = "green" if rules["number"] else "red"
        check_special.color = "green" if rules["special"] else "red"

        password_valid = rules["valid"]

        check_password_match()
        update_register_button_state()

    
    def check_password_match(e=None):
        nonlocal passwords_match

        if txt_pass.value and txt_pass.value == txt_pass_confirm.value:
            check_match.color = "green"
            passwords_match = True
        else:
            check_match.color = "red"
            passwords_match = False

        update_register_button_state()


    # Campos de cadastro
    txt_user = ft.TextField(label="Nome", width=300, on_change=lambda e: update_register_button_state())
    txt_email = ft.TextField(label="Email", width=300, on_change=lambda e: update_register_button_state())
    txt_pass = ft.TextField(
        label="Senha",
        password=True,
        width=300,
        on_change=lambda e: update_password_checks(e.control.value),
        on_focus=show_password_rules,
        on_blur=hide_password_rules,
    )
    txt_pass_confirm = ft.TextField(
        label="Confirmar Senha",
        password=True,
        width=300,
        on_change=check_password_match,
        on_focus=on_password_focus,
        on_blur=on_password_blur,
    )
    password_rules_box = ft.Container(
        visible=False,
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
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor={
                "": "#44CFA1",                
                "disabled": "#BFE9DA",       
            },
            color={
                "": "white",
                "disabled": "#EEEEEE",       
            },
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=register_click,
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


