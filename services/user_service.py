#services/user_service.py
from models.user import User
from sqlalchemy.orm import Session
from database.connection_db import SessionLocal

class UserServices:

    def __init__(self):
        self.db: Session = SessionLocal()
    
    def create_user(self, user, email, password):
        print ({user, email, password})
        try:    
            new_user = User(nome=user, email=email, password=password)
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