import logging
from models.user import User
import re
from services.user_service import UserServices 
from services.session_manager import SessionManager
from utils.security import hash_password, verify_password
from utils.security import validate_password


class UserController:
    def __init__(self):
        self.service = UserServices()

    def register_user(self, user, email, password):

        # Verificar o tamanho do nome de usuário
        if not user or len(user.strip()) < 3:
            return False, "O nome deve ter pelo menos 3 caracteres."
        
        # Verificar formato do email
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            return False, "Email inválido."

        # Verificar o tamanho da senha
        if len (password) < 8:
            return False, "A senha deve ter pelo menos 8 caracteres."
        
        rules = validate_password(password)
        if not all(rules.values()):
            return False, "A senha não atende aos critérios de segurança."

        # Verificar se o email já está cadastrado
        if self.service.get_user_by_email(email):
            return False, "Email já cadastrado."
        
        #transforma a senha em hash
        password_hash = hash_password(password)
        user = self.service.create_user(user, email, password_hash)

        # Cria usuario
        if user:
            return True, "Usuário cadastrado com sucesso."
        return False, "Erro ao cadastrar usuário."
        

    def login_user(self, email, password):
        # Aqui chama service para buscar o usuário
        user = self.service.get_user_by_email(email)
        if not user:
            return False, "Usuário não encontrado."
        
        if not verify_password(password, user.usuario_senha_hash):
            return False, "Senha incorreta."
        
        SessionManager.login(user)
        return True, f"Bem-vindo, {user.nome}!"

    def logout_user(self):
        SessionManager.logout()