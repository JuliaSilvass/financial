#services/user_service.py
from models.user import User
from sqlalchemy.orm import Session
from database.connection_db import SessionLocal

class UserServices:

    def __init__(self):
        self.db: Session = SessionLocal()
    
    def create_user(self, user):
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return True, "Usuário criado com sucesso."
        except Exception as e:
            self.db.rollback()
            return False, f"Erro ao criar usuário: {e}"
        finally:
            self.db.close()