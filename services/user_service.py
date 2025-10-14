#services/user_service.py
from models.user import User
from sqlalchemy.orm import Session
from database.connection_db import SessionLocal
import logging

class UserServices:

    def __init__(self):
        self.db: Session = SessionLocal()
    
    # Aqui o método para criar usuário
    def create_user(self, user, email, password):
        try:    
            new_user = User(nome=user, email=email, password=password)
            # TODO: Implementar hash de senha e remover do retorno no terminal os dados sensíveis
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            print ("Usuário criado com sucesso.")
            return True, "Usuário criado com sucesso."
        except Exception as e:
            self.db.rollback()
            print (f"Erro ao criar usuário: {e}")
            return False, f"Erro ao criar usuário: {e}"
        finally:
            self.db.close()

    # Aqui o método para buscar usuário por email
    def get_user_by_email(self, email: str):
        """
        Busca um usuário pelo email.
        Retorna o objeto User se encontrado, senão None.
        """
        db: Session = SessionLocal()
        try:
            user = db.query(User).filter(User.usuario_email == email).first()
            if user:
                logging.info(f"Usuário encontrado: {user.usuario_email}")
            else:
                logging.info(f"Nenhum usuário encontrado com o email: {email}")
            return user
        except Exception as e:
            logging.error(f"Erro ao buscar usuário com email {email}: {e}")
            return None
        finally:
            db.close()
            logging.info("Conexão com o banco de dados encerrada.")