import json
from login import resolve_path, load_data
from event_gestor import save_data

res_file = "res_data.json"


def load_res_data(json_file, res_needed):
    """Carga datos de recursos específicos desde el archivo JSON"""
    path = resolve_path(json_file)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            res = json.load(file)
            return res.get(res_needed, [])
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {json_file}")
        return []
    except KeyError:
        print(f"Error: Resource type '{res_needed}' not found")
        return []


def add_hotel(data):
    """Añade un nuevo hotel a los datos de recursos"""
    name = input("Hotel name: ").strip()
    location = input("Hotel location: ").strip()
    
    try:
        single_room = int(input("Single rooms: "))
        double_room = int(input("Double rooms: "))
        triple_room = int(input("Triple rooms: "))
        price = int(input("Price per pax: "))
    except ValueError:
        print("Error: Invalid numeric input.")
        return
    
    nuevo_item = {
        "name": name,
        "location": location,
        "room": [
            {"type": "Single", "count": single_room, "pax": 1},
            {"type": "Double", "count": double_room, "pax": 2},
            {"type": "Triple", "count": triple_room, "pax": 3}
        ],
        "pax_price": price
    }
    data["hotels"].append(nuevo_item)
    save_data("res_data", data)
    print("Hotel added successfully.")


def add_car(data):
    """Añade o actualiza un tipo de coche en los datos de recursos"""
    car_type = input("Car type (sedan/van/bus/motorcycle): ").strip().lower()
    
    try:
        qty = int(input("Number of cars to add (negative to subtract): "))
    except ValueError:
        print("Error: Invalid number entered.")
        return

    cars = data.get("cars", [])
    
    # Buscar si el tipo de coche ya existe
    for car in cars:
        if car.get("type", "").lower() == car_type:
            old = car.get("count", 0)
            car["count"] = max(0, old + qty)
            save_data("res_data", data)
            print(f"Updated '{car_type}' count: {old} -> {car['count']}")
            return

    # Si no existe, ofrecer crearlo
    create = input(f"Car type '{car_type}' not found. Create new entry? (y/n): ").strip().lower()
    if create == 'y':
        try:
            price_per_day = int(input("Price per day: "))
            seats = int(input("Number of seats: "))
            license_type = input("License type: ").strip()
        except ValueError:
            print("Error: Invalid numeric input.")
            return
        
        new_car = {
            "type": car_type,
            "price_per_day": price_per_day,
            "seats": seats,
            "count": max(0, qty),
            "licence_type": license_type
        }
        data["cars"].append(new_car)
        save_data("res_data", data)
        print(f"Created new car type '{car_type}' with count {new_car['count']}")


def add_driver(data):
    """Añade un nuevo chofer a los datos de recursos"""
    name = input("Driver name: ").strip()
    license_type = input("License type: ").strip()
    ci = input("CI: ").strip()
    
    if not all([name, license_type, ci]):
        print("Error: All fields are required.")
        return
    
    nuevo = {"name": name, "license_type": license_type, "CI": ci}
    data["chofer"].append(nuevo)
    save_data("res_data", data)
    print("Driver added successfully.")


def save_res_data(json_file, res_needed):
    """Interfaz para guardar datos de recursos (hotels, cars, drivers)"""
    data = load_data(json_file)
    res_needed = res_needed.lower().strip()
    
    if res_needed == "hotels":
        add_hotel(data)
    elif res_needed == "cars":
        add_car(data)
    elif res_needed in ("chofer", "chofers", "drivers"):
        add_driver(data)
    else:
        print(f"Error: Unknown resource type '{res_needed}'. Use 'hotels', 'cars', or 'chofer'.")


def check_res(json_file, res_needed=None):
    """Muestra datos de recursos de forma legible"""
    try:
        if res_needed:
            res = load_res_data(json_file, res_needed)
        else:
            res = load_data(json_file)
    except Exception as e:
        print(f"Error loading resource: {e}")
        return

    if res_needed is None:
        # Mostrar resumen de todos los recursos
        if isinstance(res, dict):
            print("\n--- Resources Summary ---")
            for k, v in res.items():
                try:
                    length = len(v)
                except Exception:
                    length = 'N/A'
                print(f"  {k}: {length} item(s)")
        else:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    if not res:
        print(f"No resource '{res_needed}' found or it's empty.")
        return

    # Mostrar lista de recursos de forma legible
    if isinstance(res, list):
        print(f"\n--- {res_needed.capitalize()} ---")
        for i, item in enumerate(res, start=1):
            print(f"\n[{i}]")
            if isinstance(item, dict):
                for key, val in item.items():
                    if isinstance(val, list):
                        print(f"  {key}:")
                        for sub in val:
                            if isinstance(sub, dict):
                                sub_items = ', '.join(f"{sk}: {sv}" for sk, sv in sub.items())
                                print(f"    - {sub_items}")
                            else:
                                print(f"    - {sub}")
                    else:
                        print(f"  {key}: {val}")
            else:
                print(f"  {item}")
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))


def _load_reservations():
    """Carga las reservaciones desde el archivo JSON"""
    path = resolve_path("reservations.json")
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"vehicle_reservations": [], "hotel_reservations": []}
    except json.JSONDecodeError:
        print("Error: Invalid JSON in reservations.json")
        return {"vehicle_reservations": [], "hotel_reservations": []}


def _save_reservations(reservations):
    """Guarda las reservaciones en el archivo JSON"""
    path = resolve_path("reservations.json")
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(reservations, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving reservations: {e}")
        return False


def cancel_reservation(res_id, res_type='vehicle'):
    """
    Cancela una reservación por su ID.
    
    Args:
        res_id: El ID de la reservación a cancelar (timestamp de created_at)
        res_type: Tipo de reservación ('vehicle' o 'hotel')
    
    Returns:
        True si la reservación fue cancelada exitosamente, False en caso contrario
        
    Ejemplo:
        cancel_reservation("2026-01-01T23:52:32.326678", "vehicle")
    """
    reservations = _load_reservations()
    key = 'vehicle_reservations' if res_type == 'vehicle' else 'hotel_reservations'
    
    if key not in reservations:
        print(f"Error: Reservation type '{res_type}' not found")
        return False
    
    original_count = len(reservations[key])
    reservations[key] = [r for r in reservations[key] if r.get('id') != res_id]
    
    if len(reservations[key]) < original_count:
        if _save_reservations(reservations):
            print(f"✓ Reservation cancelled successfully. ID: {res_id}")
            return True
        else:
            print("Error saving changes.")
            return False
    
    print(f"✗ No reservation found with ID: {res_id}")
    return False