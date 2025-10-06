import flet as ft

def login_page(page: ft.Page):
    
    # Campos de usuário e senha
    txt_email = ft.TextField(label="Email", width=300)
    txt_pass = ft.TextField(label="Senha", password=True, width=300)

    # Função do botão de login
    def login_click(e):
        user = txt_email.value
        password = txt_pass.value
        # Aqui você chama a função do controller para autenticar
        print(f"Tentando login: {user} / {password}")
        page.snack_bar = ft.SnackBar(ft.Text(f"Bem-vindo, {user}!"))
        page.snack_bar.open = True
        page.update()

    #Função do botão de voltar para home
    def backToHome_click(e):
        page.go("/")

    # Botão de login
    btn_login = ft.ElevatedButton("Login", on_click=login_click)

    # Botão de Voltar para Home
    btn_backToHome = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="white",
        bgcolor="#44CFA1",
        on_click=backToHome_click
    )

    # Retornar a View com os controles
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
                        btn_backToHome],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        ],
        horizontal_alignment="center",
        vertical_alignment="center"
    )

