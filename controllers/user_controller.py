import logging
from models.user import User
from services.user_service import UserServices 
from services.session_manager import SessionManager

class UserController:
    def __init__(self):
        self.service = UserServices()

    def register_user(self, user, email, password):
        
        # Verificar o tamanho da senha
        if len (password) < 8:
            return False, "A senha deve ter pelo menos 8 caracteres."
        
        # Verificar se o email já está cadastrado
        # existing_user = self.service.get_user_by_email(user.email)
        # if existing_user:   
        #     return False, "Email já cadastrado."

        #Cria usuário
        user = self.service.create_user(user=user,email=email,password=password) 
        if user:
            return True, "Usuário cadastrado com sucesso."
        else:
            return False, "Erro ao cadastrar usuário."
        

    def login_user(self, email, password):
        # Aqui chama service para buscar o usuário
        user = self.service.get_user_by_email(email)
        if not user:
            return False, "Usuário não encontrado."
        
        if user.usuario_senha_hash != password:  
            return False, "Senha incorreta."
        
        SessionManager.login(user)
        return True, f"Bem-vindo, {user.nome}!"

    def logout_user(self):
        SessionManager.logout()