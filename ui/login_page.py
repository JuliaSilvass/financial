import flet as ft

def login_page(page: ft.Page):
    
    # Campos de usuário e senha
    txt_user = ft.TextField(label="Usuário", width=300)
    txt_pass = ft.TextField(label="Senha", password=True, width=300)

    # Função do botão de login
    def login_click(e):
        user = txt_user.value
        password = txt_pass.value
        # Aqui você chama a função do controller para autenticar
        print(f"Tentando login: {user} / {password}")
        page.snack_bar = ft.SnackBar(ft.Text(f"Bem-vindo, {user}!"))
        page.snack_bar.open = True
        page.update()

    # Botão de login
    btn_login = ft.ElevatedButton("Login", on_click=login_click)

    # Retornar a View com os controles
    return ft.View(
        route="/login",
        controls=[
            ft.Column(
                controls=[txt_user, txt_pass, btn_login],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        ],
        horizontal_alignment="center",
        vertical_alignment="center"
    )
