from database.connection import connect_to_database
from controllers.user_controller import UserController
from utils.security import hash_password
from models.user import User

conn = connect_to_database()
controller = UserController(conn)

# criação de usuário
new_user = User(name="Julia4", email="julia4@gmail.com", password=hash_password("123456"))
controller.create_user(new_user)

# consulta de usuário por email
# user = controller.get_user_by_email("julia@gmail.com")



conn.close()
