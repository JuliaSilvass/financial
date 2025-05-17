import bcrypt

def hash_password(password: str) -> str:
    """"Hash a password using bcrypt."""

    # tranformando a senha em bytes
    password = password.encode('utf-8')
    # gerando o salt
    salt = bcrypt.gensalt()

    hash_password = bcrypt.hashpw(password, salt)
    
    # transformando o hash em string
    return hash_password.decode('utf-8')