from database.connection import connect_to_database
from controllers.user_controller import UserController
from models.user import User

conn = connect_to_database()
controller = UserController(conn)

new_user = User(name="Julia2", email="julia@gmail.com", password="123456")
controller.create_user(new_user)

user = controller.get_user_by_email("julia@gmail.com")

conn.close()
