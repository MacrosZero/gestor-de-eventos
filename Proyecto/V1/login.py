import json
import os


user_file = "login.json"


def resolve_path(json_file):
    """Devuelve el path absoluto de un archivo JSON en la misma carpeta"""
    return os.path.join(os.path.dirname(__file__), json_file)


def load_data(json_file):
    """Carga datos desde un archivo JSON. Retorna una lista de usuarios o dict de recursos"""
    path = resolve_path(json_file)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Si tiene estructura {"users": [...]}, retorna la lista
            if isinstance(data, dict) and 'users' in data:
                return data.get('users', [])
            return data
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        return [] if json_file == user_file else {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {json_file}")
        return [] if json_file == user_file else {}


def save_login_data(json_file, data):
    """Guarda datos en un archivo JSON. Envuelve listas en {"users": ...}"""
    path = resolve_path(json_file)
    try:
        to_write = data if isinstance(data, dict) else {"users": data}
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(to_write, file, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error: Could not save to {json_file}: {e}")


def save_user_data(user_file, username, password):
    """Guarda un nuevo usuario o muestra error si ya existe"""
    username = username.lower().strip()
    password = password.strip()
    
    if not username or not password:
        print("Error: Username and password cannot be empty.")
        return
    
    users = load_data(user_file)
    
    # Verificar si el usuario ya existe
    if any(user.get("username", "") == username for user in users):
        print("Error: User already exists.")
        return
    
    users.append({"username": username, "password": password, "role": "user"})
    save_login_data(user_file, users)
    print("User registered successfully.")


def make_admin(user_file, username=None):
    """Promueve un usuario a rol de administrador"""
    if username is None:
        username = input("Enter username to make admin: ").lower().strip()
    else:
        username = str(username).lower().strip()
    
    if not username:
        print("Error: Username cannot be empty.")
        return
    
    users = load_data(user_file)
    
    for user in users:
        if user.get("username", "") == username:
            user["role"] = "admin"
            save_login_data(user_file, users)
            print(f"User '{username}' promoted to admin.")
            return
    
    print(f"Error: User '{username}' does not exist.")


def login(username=None, password=None):
    """Autentica un usuario. Retorna tupla (username, password, role) o None"""
    if username is None:
        username = input("Enter username: ").lower().strip()
    else:
        username = str(username).lower().strip()
    
    if password is None:
        password = input("Enter password: ").strip()
    else:
        password = str(password).strip()
    
    if not username or not password:
        print("Error: Username and password cannot be empty.")
        return None
    
    users = load_data(user_file)
    
    for user in users:
        if user.get('username', '') == username:
            if user.get('password') == password:
                print("Login successful.")
                return (user.get('username'), user.get('password'), user.get('role'))
            else:
                print("Error: Incorrect password.")
                return None
    
    print("Error: User not found.")
    return None


def display_user_data(username, role):
    """Muestra datos de usuarios (admin ve todos, usuario ve solo su perfil)"""
    users = load_data(user_file)
    
    if role == 'admin':
        if not users:
            print("No users found.")
            return
        
        print("\n--- All Users ---")
        for user in users:
            print(f"Username: {user.get('username')}")
            print(f"Role: {user.get('role')}")
            print("---")
    else:
        for user in users:
            if user.get('username', '') == username:
                print(f"\n--- Your Profile ---")
                print(f"Username: {user.get('username')}")
                print(f"Role: {user.get('role')}")
                return
        print("Error: User profile not found.")