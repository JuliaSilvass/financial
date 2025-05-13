import logging
from models.user import User

class UserController:
    def __init__(self, conn):
        self.conn = conn

    def create_user(self, user: User):

        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO user_financial (user_name, user_email, user_password_hash) VALUES (%s, %s, %s)"
            cursor.execute(query, (user.name, user.email, user.password))
            self.conn.commit()
            cursor.close()
            logging.info("Usuário criado com sucesso.")
            return True, "Usuário criado com sucesso."
        except Exception as e:
            logging.error("erro ao criar usuário: %s", e)
            self.conn.rollback()
            cursor.close()
            return False, "Erro ao criar usuário."
        finally:
            cursor.close()
            self.conn.close()
            logging.info("Conexão com o banco de dados fechada.")
        
    def get_user_by_email(self, user_email: str):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM user_financial WHERE user_email = %s"
            cursor.execute(query, (user_email,))
            user = cursor.fetchone()
            cursor.close()
            logging.info("Usuário encontrado com sucesso.")
            return True, "Usuário encontrado com sucesso."
        except Exception as e:
            logging.error("Erro ao encontrar usuário: %s", e)
            cursor.close()
            return False, "Erro ao encontrar usuário."
        finally: 
            cursor.close()
            self.conn.close()
            logging.info("Conexão com o banco de dados fechada.")