import logging
from models.user import User
from services.user_service import UserServices 

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
        

    # def get_user_by_email(self, user_email: str):
    #     try:
    #         cursor = self.conn.cursor()
    #         query = "SELECT * FROM user_financial WHERE user_email = %s"
    #         cursor.execute(query, (user_email,))
    #         user = cursor.fetchone()
    #         cursor.close()
    #         logging.info("Usuário encontrado com sucesso.")
    #         return True, "Usuário encontrado com sucesso."
    #     except Exception as e:
    #         logging.error("Erro ao encontrar usuário: %s", e)
    #         cursor.close()
    #         return False, "Erro ao encontrar usuário."
    #     finally: 
    #         cursor.close()
    #         self.conn.close()
    #         logging.info("Conexão com o banco de dados fechada.")