import json
from datetime import datetime, timedelta
from login import resolve_path, load_data


def save_data(json_file, data):
    """Guarda datos en un archivo JSON"""
    path = resolve_path(json_file)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving to {json_file}: {e}")


def list_available_cars(res_file='res_data'):
    """Retorna lista de coches disponibles (count > 0)"""
    data = load_data(res_file)
    cars = data.get('cars', [])
    return [c for c in cars if c.get('count', 0) > 0]


def list_available_drivers(res_file='res_data'):
    """Retorna lista de choferes disponibles"""
    data = load_data(res_file)
    return data.get('chofer', [])



def parse_date(date_str):
    """Parsea fecha en 'YYYY-MM-DD' o formato ISO"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return datetime.fromisoformat(date_str)



def is_resource_available(resource_name, resource_type, start_req, end_req, total_inventory, reservations_list):
    """
    Verifica si un recurso está disponible en un rango de fechas.
    
    Args:
        resource_name: Nombre del recurso (hotel name o car type)
        resource_type: Tipo de recurso (room_type para hoteles, car_type para autos)
        start_req: Fecha de inicio (datetime object)
        end_req: Fecha de fin (datetime object)
        total_inventory: Cantidad total disponible del recurso
        reservations_list: Lista de reservaciones
        
    Returns:
        True si hay disponibilidad, False si está completamente ocupado
    """
    occupied = 0
    for res in reservations_list:
        match_resource = (res.get('hotel') == resource_name and res.get('room_type') == resource_type) or \
                         (res.get('car_type') == resource_type)
        
        if match_resource:
            res_start = parse_date(res['start'])
            res_end = parse_date(res['end'])
            
            if start_req < res_end and res_start < end_req:
                occupied += 1
                
    return (total_inventory - occupied) > 0


def load_reservations(file='reservations.json'):
    """Carga las reservas garantizando la estructura por defecto"""
    return load_data(file) or {"vehicle_reservations": [], "hotel_reservations": []}


def save_reservations(reservations, file='reservations.json'):
    """Guarda el dict de reservas en fichero"""
    save_data(file, reservations)


def find_next_available_slot(resource_name, resource_type, duration_days, reservation_type='vehicle',
                             res_data_file='res_data', reservations_file='reservations.json'):
    """Encuentra el próximo slot disponible para un recurso"""
    reservations = load_reservations(reservations_file)
    data = load_data(res_data_file)
    
    total_inventory = 0
    if reservation_type == 'vehicle':
        cars = data.get('cars', [])
        car = next((c for c in cars if c.get('type', '').lower() == resource_name.lower()), None)
        if car:
            total_inventory = car.get('count', 0)
        reservations_list = reservations.get('vehicle_reservations', [])
    else:  # hotel
        hotels = data.get('hotels', [])
        hotel = next((h for h in hotels if h.get('name', '').lower() == resource_name.lower()), None)
        if hotel:
            for room in hotel.get('room', []):
                if room.get('type', '').lower() == resource_type.lower():
                    total_inventory = room.get('count', 0)
                    break
        reservations_list = reservations.get('hotel_reservations', [])
    
    if total_inventory <= 0:
        return None
    
    start_search = datetime.now().date()
    max_search_days = 365
    
    for offset in range(max_search_days):
        start_candidate = start_search + timedelta(days=offset)
        end_candidate = start_candidate + timedelta(days=duration_days)
        
        if is_resource_available(resource_name, resource_type,
                                datetime.combine(start_candidate, datetime.min.time()),
                                datetime.combine(end_candidate, datetime.min.time()),
                                total_inventory, reservations_list):
            return (start_candidate.strftime('%Y-%m-%d'), end_candidate.strftime('%Y-%m-%d'))
    
    return None


def rent_vehicle(user, car_type, start_date, end_date, need_driver=None,
                 res_file='res_data', reservations_file='reservations.json'):
    """Reserva un vehículo y registra la reserva"""
    data = load_data(res_file)
    cars = data.get('cars', [])
    car = next((c for c in cars if c.get('type', '').lower() == car_type.lower()), None)
    if not car:
        return (False, f"Car type '{car_type}' not found")

    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
    except Exception as e:
        return (False, f"Invalid date format: {e}")

    if end < start:
        return (False, "End date must be after start date")

    reservations = load_reservations(reservations_file)
    vehicle_reservations = reservations.get('vehicle_reservations', [])
    
    if not is_resource_available(car_type, car_type, start, end, car.get('count', 0), vehicle_reservations):
        duration_days = (end - start).days or 1
        next_slot = find_next_available_slot(car_type, car_type, duration_days, 'vehicle', res_file, reservations_file)
        if next_slot:
            return (False, f"No available '{car_type}' cars for requested dates. Next available: {next_slot[0]} to {next_slot[1]}")
        else:
            return (False, f"No available '{car_type}' cars for requested dates")

    is_motorcycle = car_type.lower() == 'motorcycle'
    if need_driver is None:
        need_driver = not is_motorcycle
    
    driver = None
    if need_driver:
        choferes = data.get('chofer', [])
        if not choferes:
            return (False, f"No drivers available for '{car_type}' booking")
        
        required_license = car.get('licence_type')
        if required_license:
            driver = next((d for d in choferes if d.get('license_type', '').upper() == str(required_license).upper()), None)
            if not driver:
                return (False, f"No available driver with licence type '{required_license}' for '{car_type}'")
        else:
            driver = choferes[0]

    days = (end - start).days or 1
    price_per_day = car.get('price_per_day', 0)
    total_price = price_per_day * days
    created_at = datetime.now().isoformat()

    entry = {
        "id": created_at,
        "user": user,
        "car_type": car_type,
        "driver": (driver.get('name') if isinstance(driver, dict) else None),
        "start": start.isoformat(),
        "end": end.isoformat(),
        "days": days,
        "total_price": total_price,
        "created_at": created_at
    }
    reservations.setdefault('vehicle_reservations', []).append(entry)
    save_reservations(reservations, reservations_file)

    return (True, entry)


def reserve_hotel(user, hotel_name, room_type, start_date, end_date, pax=1,
                  res_file='res_data', reservations_file='reservations.json'):
    """Reserva una habitación y registra la reserva"""
    data = load_data(res_file)
    hotels = data.get('hotels', [])
    hotel = next((h for h in hotels if h.get('name', '').lower() == hotel_name.lower()), None)
    if not hotel:
        return (False, f"Hotel '{hotel_name}' not found")

    room = None
    for r in hotel.get('room', []):
        if r.get('type', '').lower() == room_type.lower():
            room = r
            break

    if not room:
        return (False, f"Room type '{room_type}' not found in hotel '{hotel_name}'")

    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
    except Exception as e:
        return (False, f"Invalid date format: {e}")

    if end < start:
        return (False, "End date must be after start date")

    reservations = load_reservations(reservations_file)
    hotel_reservations = reservations.get('hotel_reservations', [])
    
    if not is_resource_available(hotel_name, room_type, start, end, room.get('count', 0), hotel_reservations):
        duration_days = (end - start).days or 1
        next_slot = find_next_available_slot(hotel_name, room_type, duration_days, 'hotel', res_file, reservations_file)
        if next_slot:
            return (False, f"No rooms of type '{room_type}' available for requested dates. Next available: {next_slot[0]} to {next_slot[1]}")
        else:
            return (False, f"No rooms of type '{room_type}' available for requested dates")

    days = (end - start).days or 1
    pax_price = hotel.get('pax_price', 0)
    total_price = pax_price * pax * days
    created_at = datetime.now().isoformat()

    entry = {
        "id": created_at,
        "user": user,
        "hotel": hotel_name,
        "room_type": room_type,
        "pax": pax,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "days": days,
        "total_price": total_price,
        "created_at": created_at
    }
    reservations.setdefault('hotel_reservations', []).append(entry)
    save_reservations(reservations, reservations_file)
    return (True, entry)


def list_reservations(reservations_file='reservations.json'):
    """Retorna el dict completo de reservas"""
    return load_reservations(reservations_file)


def print_user_reservations(user, reservations_file='reservations.json'):
    """Imprime las reservas de un usuario en formato legible con IDs para cancelación"""
    reservations = load_reservations(reservations_file)
    vehicle = [r for r in reservations.get('vehicle_reservations', []) if r.get('user') == user]
    hotel = [r for r in reservations.get('hotel_reservations', []) if r.get('user') == user]

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


def rent_vehicle_cli(user):
    """Interfaz CLI para reservar un vehículo"""
    car_type = input("Car type to rent: ").strip()
    start = input("Start date (YYYY-MM-DD): ").strip()
    end = input("End date (YYYY-MM-DD): ").strip()
    need_driver = input("Need driver? (y/n): ").strip().lower() == 'y'
    
    ok, result = rent_vehicle(user, car_type, start, end, need_driver)
    if ok:
        print("\n✓ Reservation created:")
        print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print(f"✗ Error: {result}")


def reserve_hotel_cli(user):
    """Interfaz CLI para reservar hotel"""
    hotel = input("Hotel name: ").strip()
    room = input("Room type (Single/Double/Triple): ").strip()
    
    try:
        pax = int(input("Pax count: "))
    except ValueError:
        print("Error: Invalid pax count.")
        return
    
    start = input("Start date (YYYY-MM-DD): ").strip()
    end = input("End date (YYYY-MM-DD): ").strip()
    
    ok, result = reserve_hotel(user, hotel, room, start, end, pax)
    if ok:
        print("\n✓ Hotel reservation created:")
        print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print(f"✗ Error: {result}")


def cancel_reservation_cli(user):
    """Interfaz CLI para cancelar una reservación"""
    from res_mgmt import cancel_reservation
    
    print_user_reservations(user)
    
    res_id = input("\nEnter the ID of the reservation to cancel: ").strip()
    if not res_id:
        print("✗ No ID provided.")
        return
    
    res_type = input("Is it a vehicle or hotel reservation? (vehicle/hotel): ").strip().lower()
    if res_type not in ('vehicle', 'hotel'):
        print("✗ Invalid reservation type.")
        return
    
    cancel_reservation(res_id, res_type)