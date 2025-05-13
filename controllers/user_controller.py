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
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            self.conn.rollback()
            cursor.close()