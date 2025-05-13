from database.connection import connect_to_database
from controllers.user_controller import UserController
from models.user import User

conn = connect_to_database()
controller = UserController(conn)

new_user = User(name="Julia", email="julia@email.com", password="123456")
controller.create_user(new_user)

conn.close()
