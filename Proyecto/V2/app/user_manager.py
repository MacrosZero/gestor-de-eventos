"""
User Manager - Gestiona autenticación y usuarios
"""
from database import DatabaseManager
from typing import Tuple, Optional, List, Dict


class UserManager:
    """Gestiona usuarios, autenticación y roles"""
    
    def __init__(self, db: DatabaseManager):
        """
        Inicializa el gestor de usuarios.
        
        Args:
            db: Instancia de DatabaseManager
        """
        self.db = db
        self.user_file = "login.json"
    
    def register_user(self, username: str, password: str) -> bool:
        """Registra un nuevo usuario y lo persiste en `login.json`.

        Comportamiento:
            - Normaliza `username` a minúsculas y recorta espacios.
            - Valida que `username` y `password` no estén vacíos.
            - Comprueba que el usuario no exista ya en la lista.
            - Añade al usuario con rol `'user'` y guarda usando `_save_users`.

        Returns:
            True si el usuario fue agregado correctamente, False si ya existía o hubo error.
        """
        username = username.lower().strip()
        password = password.strip()
        
        if not username or not password:
            print("Error: Username and password cannot be empty.")
            return False
        
        users = self._get_users()
        
        if any(user.get("username", "") == username for user in users):
            print("Error: User already exists.")
            return False
        
        users.append({"username": username, "password": password, "role": "user"})
        return self._save_users(users)
    
    def login(self, username: str = None, password: str = None) -> Optional[Tuple[str, str, str]]:
        """Autentica un usuario contra los datos almacenados.

        Flujo:
            - Si `username` o `password` son None se solicitan por consola.
            - Busca el usuario en la lista y compara la contraseña.

        Returns:
            Tupla `(username, password, role)` si la autenticación fue exitosa,
            o `None` si falla (usuario no existe o contraseña incorrecta).
        """
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
        
        users = self._get_users()
        
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
    
    def make_admin(self, username: str = None) -> bool:
        """Promueve el usuario indicado a rol 'admin'.

        Args:
            username: Nombre de usuario a promover. Si es None se solicita por consola.

        Comportamiento:
            - Busca el usuario en la lista; si existe asigna `role = 'admin'` y guarda.

        Returns:
            True si la promoción y el guardado se realizaron con éxito, False en caso contrario.
        """
        if username is None:
            username = input("Enter username to make admin: ").lower().strip()
        else:
            username = str(username).lower().strip()
        
        if not username:
            print("Error: Username cannot be empty.")
            return False
        
        users = self._get_users()
        
        for user in users:
            if user.get("username", "") == username:
                user["role"] = "admin"
                return self._save_users(users)
        
        print(f"Error: User '{username}' does not exist.")
        return False
    
    def display_user_data(self, username: str, role: str) -> None:
        """Muestra en consola datos de usuarios.

        Comportamiento:
            - Si `role` es 'admin' imprime todos los usuarios y sus roles.
            - Si `role` es 'user' imprime solo el perfil del `username` dado.

        Args:
            username: Nombre del usuario que solicita ver datos.
            role: Rol del usuario actual, controla el alcance de la visualización.
        """
        users = self._get_users()
        
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
    
    def get_all_users(self) -> List[Dict]:
        """Retorna la lista completa de usuarios almacenados.

        Nota: este método delega en `_get_users` y devuelve una lista (vacía si no hay usuarios).
        """
        return self._get_users()
    
    # ===== Métodos Privados (Gestión de formato) =====
    
    def _get_users(self) -> List[Dict]:
        """Carga y retorna la lista interna de usuarios desde `login.json`.

        Formatos soportados en el archivo:
            - `{ "users": [...] }` (estructura preferida)
            - Lista directa `[...]`

        Returns:
            Lista de usuarios (cada uno es un dict con keys `username`, `password`, `role`).
        """
        data = self.db.load_json_file(self.user_file)
        
        # Si tiene estructura {"users": [...]}, extrae la lista
        if isinstance(data, dict) and 'users' in data:
            return data.get('users', [])
        
        # Si es una lista directa, retorna
        if isinstance(data, list):
            return data
        
        return []
    
    def _save_users(self, users: List[Dict]) -> bool:
        """Guarda la lista de usuarios en `login.json` con el formato {"users": [...]}.

        Args:
            users: Lista de diccionarios de usuario que se persistirán.

        Returns:
            True si el guardado fue exitoso, False si falló.
        """
        formatted_data = {"users": users}
        if self.db.save(self.user_file, formatted_data):
            print("User data saved successfully.")
            return True
        return False
    
    def get_all_users(self) -> List[Dict]:
        """(Alias) Retorna la lista de todos los usuarios usando `DatabaseManager.load`.

        Nota: existe otro método `get_all_users` que delega en `_get_users`; este
        método actúa como un alias que devuelve la carga cruda del archivo.
        """
        return self.db.load(self.user_file, [])
