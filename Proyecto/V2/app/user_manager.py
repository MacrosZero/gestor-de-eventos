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
        """
        Registra un nuevo usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            True si se registró exitosamente, False si ya existe
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
        """
        Autentica un usuario.
        
        Args:
            username: Nombre de usuario (si es None, se pide por input)
            password: Contraseña (si es None, se pide por input)
            
        Returns:
            Tupla (username, password, role) si es exitoso, None en caso contrario
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
        """
        Promueve un usuario a administrador.
        
        Args:
            username: Nombre de usuario (si es None, se pide por input)
            
        Returns:
            True si se promovió exitosamente, False en caso contrario
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
        """
        Muestra datos de usuarios.
        
        Args:
            username: Nombre del usuario actual
            role: Rol del usuario (admin o user)
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
        """
        Obtiene todos los usuarios.
        
        Returns:
            Lista de diccionarios con datos de usuarios
        """
        return self._get_users()
    
    # ===== Métodos Privados (Gestión de formato) =====
    
    def _get_users(self) -> List[Dict]:
        """
        Obtiene la lista de usuarios desde el archivo.
        
        Returns:
            Lista de usuarios (vacía si el archivo no existe)
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
        """
        Guarda la lista de usuarios con formato {"users": [...]}
        
        Args:
            users: Lista de usuarios a guardar
            
        Returns:
            True si se guardó exitosamente
        """
        formatted_data = {"users": users}
        if self.db.save(self.user_file, formatted_data):
            print("User data saved successfully.")
            return True
        return False
    
    def get_all_users(self) -> List[Dict]:
        """Retorna lista de todos los usuarios"""
        return self.db.load(self.user_file, [])
