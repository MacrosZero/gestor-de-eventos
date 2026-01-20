"""
Menu Manager - Gestiona los menús del sistema
"""
import json
from typing import Optional, Tuple


class MenuManager:
    """Gestiona los menús interactivos del sistema"""
    
    def __init__(self, user_mgr: 'UserManager', resource_mgr: 'ResourceManager', 
                 reservation_mgr: 'ReservationManager'):
        """
        Inicializa el gestor de menús.
        
        Args:
            user_mgr: Instancia de UserManager
            resource_mgr: Instancia de ResourceManager
            reservation_mgr: Instancia de ReservationManager
        """
        self.user_mgr = user_mgr
        self.resource_mgr = resource_mgr
        self.reservation_mgr = reservation_mgr
        self.current_user = None
        self.current_role = None
    
    def display_menu(self, options: list) -> None:
        """Imprime en consola las `options` proporcionadas, una por línea.

        Args:
            options: Lista de strings que representan las opciones del menú.
        """
        for option in options:
            print(option)
    
    def admin_menu(self, username: str, role: str) -> None:
        """Menú interactivo para usuarios con rol 'admin'.

        Opciones principales:
            1. View Users Data
            2. Make Admin
            3. Manage Resources
            4. View Resources Data
            5. Logout

        Notas:
            - Esta función es el bucle principal del menú de administradores y
              realiza llamadas a `UserManager` y `ResourceManager` según la opción.
        """
        menu_options = [
            "1. View Users Data",
            "2. Make Admin",
            "3. Manage Resources",
            "4. View Resources Data",
            "5. Logout"
        ]
        
        while True:
            self.display_menu(menu_options)
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self.user_mgr.display_user_data(username, role)
            elif choice == "2":
                self.user_mgr.make_admin()
            elif choice == "3":
                self._manage_resources_menu()
            elif choice == "4":
                self._view_resources_menu()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def user_menu(self, username: str, role: str) -> None:
        """Menú interactivo para usuarios con rol 'user'.

        Opciones incluyen ver perfil, rentar vehículo, reservar hotel, ver y cancelar reservas.
        """
        menu_options = [
            "1. View User Data",
            "2. Rent Vehicle",
            "3. Reserve Hotel",
            "4. View My Reservations",
            "5. Cancel Reservation",
            "6. Logout"
        ]
        
        while True:
            self.display_menu(menu_options)
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self.user_mgr.display_user_data(username, role)
            elif choice == "2":
                self._rent_vehicle_cli(username)
            elif choice == "3":
                self._reserve_hotel_cli(username)
            elif choice == "4":
                self._view_user_reservations(username)
            elif choice == "5":
                self._cancel_reservation_cli(username)
            elif choice == "6":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def main_menu(self) -> None:
        """Bucle del menú principal que permite registrarse, iniciar sesión o salir.

        - Si el usuario inicia sesión se delega al menú correspondiente por rol.
        """
        menu_options = [
            "1. Register User",
            "2. Login",
            "3. Exit"
        ]
        
        while True:
            self.display_menu(menu_options)
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self._register_user()
            elif choice == "2":
                self._login()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _register_user(self) -> None:
        """Interfaz para registrar usuarios solicitando `username` y `password` por consola.

        Llamada: delega en `UserManager.register_user`.
        """
        username = input("Enter username: ").lower().strip()
        password = input("Enter password: ").strip()
        self.user_mgr.register_user(username, password)
    
    def _login(self) -> None:
        """Solicita credenciales y, si son válidas, abre el menú apropiado por rol.

        Flujo:
            - Llama a `UserManager.login` para autenticar.
            - Si el rol es 'admin' llama a `admin_menu`, si no a `user_menu`.
        """
        result = self.user_mgr.login()
        if result:
            username, password, role = result
            if role == "admin":
                self.admin_menu(username, role)
            else:
                self.user_menu(username, role)
    
    def _manage_resources_menu(self) -> None:
        """Interfaz de menú para tareas administrativas sobre recursos.

        Opciones:
            1. Add Hotel
            2. Add Car
            3. Add Driver
            4. Back
        """
        while True:
            print("\n--- Manage Resources ---")
            print("1. Add Hotel")
            print("2. Add Car")
            print("3. Add Driver")
            print("4. Back")
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self.resource_mgr.add_hotel()
            elif choice == "2":
                self.resource_mgr.add_car()
            elif choice == "3":
                self.resource_mgr.add_driver()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _view_resources_menu(self) -> None:
        """Interfaz para visualizar distintos tipos de recursos disponibles.

        Opciones permiten ver resumen, hoteles, coches y choferes.
        """
        while True:
            print("\n--- View Resources ---")
            print("1. All Resources Summary")
            print("2. View Hotels")
            print("3. View Cars")
            print("4. View Drivers")
            print("5. Back")
            choice = input("Choose an option: ").strip()
            
            if choice == "1":
                self.resource_mgr.show_resources_summary()
            elif choice == "2":
                self.resource_mgr.show_resource_type("hotels")
            elif choice == "3":
                self.resource_mgr.show_resource_type("cars")
            elif choice == "4":
                self.resource_mgr.show_resource_type("chofer")
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _rent_vehicle_cli(self, user: str) -> None:
        """Interfaz CLI para reservar un vehículo mostrando opciones disponibles.

        Comportamiento:
            - Muestra `get_available_cars()` para que el usuario elija un tipo válido.
            - Solicita fechas y si necesita chofer.
            - Llama a `ReservationManager.rent_vehicle` y muestra el resultado.
        """
        # Mostrar tipos de coche disponibles antes de pedir la elección
        available = self.resource_mgr.get_available_cars()
        if not available:
            print("No cars available at the moment.")
            return

        print("\nAvailable car types:")
        for c in available:
            print(f" - {c.get('type')}")

        car_type = input("Choose car type to rent: ").strip()
        start = input("Start date (YYYY-MM-DD): ").strip()
        end = input("End date (YYYY-MM-DD): ").strip()
        need_driver = input("Need driver? (y/n): ").strip().lower() == 'y'

        ok, result = self.reservation_mgr.rent_vehicle(user, car_type, start, end, need_driver)
        if ok:
            print("\n✓ Reservation created:")
            print(result)
        else:
            print(f"✗ Error: {result}")
    
    def _reserve_hotel_cli(self, user: str) -> None:
        """Interfaz CLI para reservar hotel mostrando hoteles y tipos de habitación.

        Comportamiento:
            - Lista hoteles y sus `room` entries con counts antes de pedir elección.
            - Solicita pax, fechas y luego llama a `ReservationManager.reserve_hotel`.
        """
        # Mostrar hoteles y tipos de habitación disponibles
        hotels = self.resource_mgr.get_all_hotels()
        if not hotels:
            print("No hotels available at the moment.")
            return

        print("\nAvailable hotels and room types:")
        for h in hotels:
            print(f" - {h.get('name')} ({h.get('location')})")

        hotel = input("Choose hotel name: ").strip()
        room = input("Room type (Single/Double/Triple): ").strip()

        try:
            pax = int(input("Pax count: "))
        except ValueError:
            print("Error: Invalid pax count.")
            return

        start = input("Start date (YYYY-MM-DD): ").strip()
        end = input("End date (YYYY-MM-DD): ").strip()

        ok, result = self.reservation_mgr.reserve_hotel(user, hotel, room, start, end, pax)
        if ok:
            print("\n✓ Hotel reservation created:")
            print(result)
        else:
            print(f"✗ Error: {result}")
    
    def _view_user_reservations(self, user: str) -> None:
        """Muestra las reservas de un usuario"""
        vehicle, hotel = self.reservation_mgr.get_user_reservations(user)
        
        print(f"\n=== Reservations for {user} ===")
        
        print("\n-- Vehicles --")
        if not vehicle:
            print("  (no vehicle reservations)")
        else:
            for i, r in enumerate(vehicle, 1):
                drv = r.get('driver') or 'No driver'
                start = r.get('start')
                end = r.get('end')
                days = r.get('days')
                price = r.get('total_price')
                res_id = r.get('id') or r.get('created_at')
                print(f"[{i}] {r.get('car_type')} — {start} → {end} ({days} days) — ${price}")
                print(f"     Driver: {drv}")
                print(f"     🔑 ID: {res_id}")
        
        print("\n-- Hotels --")
        if not hotel:
            print("  (no hotel reservations)")
        else:
            for i, r in enumerate(hotel, 1):
                start = r.get('start')
                end = r.get('end')
                days = r.get('days')
                price = r.get('total_price')
                pax = r.get('pax')
                res_id = r.get('id') or r.get('created_at')
                print(f"[{i}] {r.get('hotel')} — {r.get('room_type')} — pax:{pax} — {start} → {end} ({days} days) — ${price}")
                print(f"     🔑 ID: {res_id}")
    
    def _cancel_reservation_cli(self, user: str) -> None:
        """Interfaz CLI para cancelar una reservación"""
        self._view_user_reservations(user)
        
        res_id = input("\nEnter the ID of the reservation to cancel: ").strip()
        if not res_id:
            print("✗ No ID provided.")
            return
        
        res_type = input("Is it a vehicle or hotel reservation? (vehicle/hotel): ").strip().lower()
        if res_type not in ('vehicle', 'hotel'):
            print("✗ Invalid reservation type.")
            return
        
        self.reservation_mgr.cancel_reservation(res_id, res_type)
