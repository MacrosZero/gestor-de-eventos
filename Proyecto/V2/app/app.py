"""
Main Application - Orquesta todas las clases del sistema
"""
from database import DatabaseManager
from user_manager import UserManager
from resource_manager import ResourceManager
from reservation_manager import ReservationManager
from menu_manager import MenuManager


class ReservationApp:
    """Aplicación principal de gestión de reservas"""
    
    def __init__(self, base_dir: str = None):
        """
        Inicializa la aplicación.
        
        Args:
            base_dir: Directorio base para los archivos JSON
        """
        # Inicializar componentes
        self.db = DatabaseManager(base_dir)
        self.user_mgr = UserManager(self.db)
        self.resource_mgr = ResourceManager(self.db)
        self.reservation_mgr = ReservationManager(self.db, self.resource_mgr)
        self.menu_mgr = MenuManager(self.user_mgr, self.resource_mgr, self.reservation_mgr)
    
    def run(self) -> None:
        """Inicia la aplicación"""
        print("\n" + "="*50)
        print("   RESERVATION MANAGEMENT SYSTEM")
        print("="*50 + "\n")
        
        try:
            self.menu_mgr.main_menu()
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            print("Thank you for using our system!")


def main():
    """Punto de entrada de la aplicación"""
    app = ReservationApp()
    app.run()


if __name__ == "__main__":
    main()
