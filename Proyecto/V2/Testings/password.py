import hashlib as ash

password='federico'
print(password)
def hashpassword(password: str) -> str:
    """Genera un hash SHA-256 para la contraseña dada.

    Args:
        password: Contraseña en texto plano."""
    
    return  print(ash.sha256(password.encode('utf-8')).hexdigest())

hashpassword(password)