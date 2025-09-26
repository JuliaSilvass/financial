from database.connection_db import test_connection
from controllers.user_controller import UserController
from utils.security import hash_password
from models.user import User


if __name__ == "__main__":
    test_connection()