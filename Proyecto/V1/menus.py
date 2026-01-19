import login
import res_mgmt
import event_gestor


def display_menu(options):
    """Muestra un menú genérico con las opciones proporcionadas"""
    for option in options:
        print(option)


def admin_menu(username=None, role=None):
    """Menú para administradores"""
    menu_options = [
        "1. View Users Data",
        "2. Manage Resources",
        "3. View Resources Data",
        "4. Logout"
    ]
    
    while True:
        display_menu(menu_options)
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            login.display_user_data(username, role)
        elif choice == "2":
            res_type = input("Resource to manage (hotels/cars/chofer): ").strip().lower()
            res_mgmt.save_res_data('res_data', res_type)
        elif choice == "3":
            res_type = input("Resource to check (hotels/cars/chofer): ").strip().lower()
            res_mgmt.check_res('res_data', res_type)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


def user_menu(username=None, role=None):
    """Menú para usuarios normales"""
    menu_options = [
        "1. View User Data",
        "2. Rent Vehicle",
        "3. Reserve Hotel",
        "4. View My Reservations",
        "5. Cancel Reservation",
        "6. Logout"
    ]
    
    while True:
        display_menu(menu_options)
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            login.display_user_data(username, role)
        elif choice == "2":
            event_gestor.rent_vehicle_cli(username)
        elif choice == "3":
            event_gestor.reserve_hotel_cli(username)
        elif choice == "4":
            event_gestor.print_user_reservations(username)
        elif choice == "5":
            event_gestor.cancel_reservation_cli(username)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


def main_menu():
    """Menú principal de la aplicación"""
    menu_options = [
        "1. Register User",
        "2. Login",
        "3. Exit"
    ]
    
    while True:
        display_menu(menu_options)
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            username = input("Enter username: ").lower().strip()
            password = input("Enter password: ").strip()
            login.save_user_data(login.user_file, username, password)
        elif choice == "2":
            result = login.login()
            if result:
                username, password, role = result
                if role == "admin":
                    admin_menu(username, role)
                else:
                    user_menu(username, role)
            else:
                print("Login failed.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()