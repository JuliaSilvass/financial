import bcrypt
import re

def hash_password(password: str) -> str:
    """"Senha hash usando bcrypt."""

    # tranformando a senha em bytes
    password = password.encode('utf-8')
    # gerando o salt
    salt = bcrypt.gensalt()

    hash_password = bcrypt.hashpw(password, salt)
    
    # transformando o hash em string
    return hash_password.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed.encode("utf-8")
        )
    except ValueError:
        # hash inválido
        return False

def validate_password(password: str) -> dict:
    rules = {
        "length": len(password) >= 8,
        "upper": bool(re.search(r"[A-Z]", password)),
        "lower": bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
    }
    rules["valid"] = all(rules.values())
    return rules

