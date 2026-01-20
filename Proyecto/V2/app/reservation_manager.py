"""
Reservation Manager - Gestiona reservas de vehículos y hoteles
"""
import json
from datetime import datetime, timedelta
from database import DatabaseManager
from typing import Tuple, Optional, List, Dict


class ReservationManager:
    """Gestiona reservas de vehículos y hoteles"""
    
    def __init__(self, db: DatabaseManager, resource_mgr: 'ResourceManager'):
        """
        Inicializa el gestor de reservas.
        
        Args:
            db: Instancia de DatabaseManager
            resource_mgr: Instancia de ResourceManager
        """
        self.db = db
        self.resource_mgr = resource_mgr
        self.reservations_file = "reservations.json"
    
    def load_reservations(self) -> Dict:
        """Carga todas las reservas desde `reservations.json`.

        Returns:
            Diccionario con claves `vehicle_reservations` y `hotel_reservations`.

        Nota:
            - Si el archivo no existe devuelve la estructura por defecto.
        """
        data = self.db.load_json_file(self.reservations_file)
        if not data:
            return {"vehicle_reservations": [], "hotel_reservations": []}
        return data
    
    def save_reservations(self, reservations: Dict) -> bool:
        """Guarda el diccionario `reservations` en el archivo de reservas.

        Args:
            reservations: Estructura con reservas de vehículos y hoteles.

        Returns:
            True si el guardado fue exitoso, False en caso de error de IO.
        """
        return self.db.save_json_file(self.reservations_file, reservations)
    
    def parse_date(self, date_str: str) -> datetime:
        """Parsea una cadena de fecha en un objeto `datetime`.

        Soporta dos formatos:
            - 'YYYY-MM-DD' (sin hora)
            - Formato ISO que incluye tiempo (por ejemplo '2026-01-01T00:00:00')

        Raises:
            ValueError si la cadena no puede ser parseada por ninguno de los
            formatos esperados. El método intenta primero '%Y-%m-%d' y luego
            `fromisoformat`.
        """
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return datetime.fromisoformat(date_str)
    
    def is_resource_available(self, resource_name: str, resource_type: str, 
                            start_req: datetime, end_req: datetime, 
                            total_inventory: int, reservations_list: List) -> bool:
        """Determina si hay al menos una unidad disponible del recurso pedido
        para el rango [start_req, end_req).

        Lógica:
            - Recorre `reservations_list` y cuenta cuántas reservas del mismo
              recurso y tipo se solapan con el rango solicitado.
            - Considera solapamiento cuando (start_req < res_end) and (res_start < end_req).
            - Retorna True si `total_inventory - ocupadas > 0`.

        Args:
            resource_name: Nombre del recurso (hotel name o car type dependiendo).
            resource_type: Tipo de recurso (para hotels indica room_type, para cars indica car_type).
            start_req, end_req: Rangos de fecha como `datetime`.
            total_inventory: Cantidad total disponible de ese recurso.
            reservations_list: Lista de reservas del tipo correspondiente.

        Returns:
            True si hay disponibilidad, False si está agotado para el rango.
        """
        occupied = 0
        for res in reservations_list:
            match_resource = (res.get('hotel') == resource_name and res.get('room_type') == resource_type) or \
                           (res.get('car_type') == resource_type)
            
            if match_resource:
                res_start = self.parse_date(res['start'])
                res_end = self.parse_date(res['end'])
                
                if start_req < res_end and res_start < end_req:
                    occupied += 1
        
        return (total_inventory - occupied) > 0
    
    def has_overlapping_vehicle_reservation(self, user: str, start_req: datetime, end_req: datetime) -> Optional[Dict]:
        """Verifica si `user` ya tiene una reserva de vehículo que se solapa con las fechas.

        Política de exclusión mutua:
            - Un usuario no puede tener más de una reserva de vehículo cuyos
              intervalos de fechas se solapen.

        Args:
            user: Nombre del usuario a comprobar.
            start_req, end_req: Intervalo solicitado como `datetime`.

        Returns:
            La reserva existente (dict) que entra en conflicto, o None si no hay conflicto.
        """
        reservations = self.load_reservations()
        vehicle_reservations = reservations.get('vehicle_reservations', [])
        
        for res in vehicle_reservations:
            # Solo revisar reservas del mismo usuario
            if res.get('user') == user:
                res_start = self.parse_date(res['start'])
                res_end = self.parse_date(res['end'])
                
                # Verificar solapamiento: (InicioA < FinB) y (InicioB < FinA)
                if start_req < res_end and res_start < end_req:
                    return res  # Hay conflicto
        
        return None  # No hay conflicto
    
    def has_overlapping_hotel_reservation(self, user: str, start_req: datetime, end_req: datetime) -> Optional[Dict]:
        """Verifica si `user` ya tiene una reserva de hotel que se solapa con las fechas.

        Política de exclusión mutua similar a la vehicular: no permitir dos reservas
        de hotel que se solapen para el mismo usuario.

        Args y Returns: ver `has_overlapping_vehicle_reservation`.
        """
        reservations = self.load_reservations()
        hotel_reservations = reservations.get('hotel_reservations', [])
        
        for res in hotel_reservations:
            # Solo revisar reservas del mismo usuario
            if res.get('user') == user:
                res_start = self.parse_date(res['start'])
                res_end = self.parse_date(res['end'])
                
                # Verificar solapamiento: (InicioA < FinB) y (InicioB < FinA)
                if start_req < res_end and res_start < end_req:
                    return res  # Hay conflicto
        
        return None  # No hay conflicto

    def find_next_available_slot(self, resource_name: str, resource_type: str, 
                                duration_days: int, reservation_type: str = 'vehicle') -> Optional[Tuple[str, str]]:
        """Busca la primera ventana continua de `duration_days` donde exista
        disponibilidad para el recurso indicado dentro del horizonte de búsqueda.

        Args:
            resource_name: Nombre del recurso (hotel name o car type).
            resource_type: Tipo específico (room type o car type según `reservation_type`).
            duration_days: Duración requerida en días.
            reservation_type: 'vehicle' o 'hotel' para elegir la fuente de reservas.

        Returns:
            Tupla (start_str, end_str) con fechas en 'YYYY-MM-DD' del primer slot
            encontrado, o None si no hay hueco en el periodo de búsqueda (365 días).
        """
        reservations = self.load_reservations()
        
        total_inventory = 0
        if reservation_type == 'vehicle':
            car = self.resource_mgr.get_car(resource_name)
            if car:
                total_inventory = car.get('count', 0)
            reservations_list = reservations.get('vehicle_reservations', [])
        else:  # hotel
            hotel = self.resource_mgr.get_hotel(resource_name)
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
            
            if self.is_resource_available(resource_name, resource_type,
                                        datetime.combine(start_candidate, datetime.min.time()),
                                        datetime.combine(end_candidate, datetime.min.time()),
                                        total_inventory, reservations_list):
                return (start_candidate.strftime('%Y-%m-%d'), end_candidate.strftime('%Y-%m-%d'))
        
        return None
    
    def rent_vehicle(self, user: str, car_type: str, start_date: str, 
                    end_date: str, need_driver: bool = None) -> Tuple[bool, str]:
                """Realiza una reserva de vehículo para `user`.

                Validaciones y efectos:
                        - Verifica que `car_type` exista en los recursos.
                        - Parsea y valida fechas; asegura que `end >= start`.
                        - Requiere que la reserva se haga con >=72 horas de antelación
                            (esto ya se valida antes de llegar aquí si se llama desde la CLI).
                        - Comprueba la política de exclusión mutua: un usuario no puede
                            reservar dos vehículos solapados.
                        - Verifica disponibilidad por inventario y, si no hay, sugiere
                            el siguiente hueco disponible.
                        - Si `need_driver` es True, busca un chofer con la licencia
                            requerida por el coche; si no hay, retorna error.

                Returns:
                        (True, entry_json) en caso de éxito (entry_json es JSON formateado de la reserva),
                        (False, mensaje_de_error) en caso de fallo.
                """
        car = self.resource_mgr.get_car(car_type)
        if not car:
            return (False, f"Car type '{car_type}' not found")
        
        try:
            start = self.parse_date(start_date)
            end = self.parse_date(end_date)
        except Exception as e:
            return (False, f"Invalid date format: {e}")
        
        if end < start:
            return (False, "End date must be after start date")

        # Validación: la reserva debe hacerse con al menos 72 horas de antelación
        min_allowed_date = (datetime.now() + timedelta(hours=72)).date()
        if start.date() < min_allowed_date:
            return (False, f"Reservations must be made at least 72 hours in advance. Earliest start date: {min_allowed_date.strftime('%Y-%m-%d')}")
        
        # VALIDACIÓN DE EXCLUSIÓN MUTUA: Verificar si el usuario ya tiene otro vehículo
        existing_vehicle = self.has_overlapping_vehicle_reservation(user, start, end)
        if existing_vehicle:
            return (False, f"CONFLICT: You already have a vehicle reservation from {existing_vehicle.get('start')} to {existing_vehicle.get('end')}. "
                          f"You cannot reserve two vehicles at the same time (Mutual Exclusion Policy).")
        
        reservations = self.load_reservations()
        vehicle_reservations = reservations.get('vehicle_reservations', [])
        
        if not self.is_resource_available(car_type, car_type, start, end, car.get('count', 0), vehicle_reservations):
            duration_days = (end - start).days or 1
            next_slot = self.find_next_available_slot(car_type, car_type, duration_days, 'vehicle')
            if next_slot:
                return (False, f"No available '{car_type}' cars. Next available: {next_slot[0]} to {next_slot[1]}")
            else:
                return (False, f"No available '{car_type}' cars for requested dates")
        
        is_motorcycle = car_type.lower() == 'motorcycle'
        if need_driver is None:
            need_driver = not is_motorcycle
        
        driver = None
        if need_driver:
            drivers = self.resource_mgr.get_all_drivers()
            if not drivers:
                return (False, f"No drivers available for '{car_type}' booking")
            
            required_license = car.get('licence_type')
            if required_license:
                driver = self.resource_mgr.find_driver_by_license(required_license)
                if not driver:
                    return (False, f"No available driver with licence type '{required_license}'")
            else:
                driver = drivers[0]
        
        days = (end - start).days or 1
        price_per_day = car.get('price_per_day', 0)
        total_price = price_per_day * days
        created_at = datetime.now().isoformat()
        
        entry = {
            "id": created_at,
            "user": user,
            "car_type": car_type,
            "driver": driver.get('name') if isinstance(driver, dict) else None,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "days": days,
            "total_price": total_price,
            "created_at": created_at
        }
        
        reservations.setdefault('vehicle_reservations', []).append(entry)
        self.save_reservations(reservations)
        
        return (True, json.dumps(entry, ensure_ascii=False, indent=2))
    
    def reserve_hotel(self, user: str, hotel_name: str, room_type: str, 
                     start_date: str, end_date: str, pax: int = 1) -> Tuple[bool, str]:
        """Reserva una habitación de hotel para `user`.

        Validaciones y efectos:
            - Verifica la existencia del hotel y del tipo de habitación.
            - Parsea y valida fechas; asegura que `end >= start`.
            - Requiere que la reserva se haga con >=72 horas de antelación.
            - Aplica la política de exclusión mutua para reservas de hotel.
            - Comprueba inventario de habitaciones y sugiere el siguiente hueco si no hay disponibilidad.

        Returns:
            (True, entry_json) en caso de éxito, (False, mensaje_de_error) en caso de fallo.
        """
        hotel = self.resource_mgr.get_hotel(hotel_name)
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
            start = self.parse_date(start_date)
            end = self.parse_date(end_date)
        except Exception as e:
            return (False, f"Invalid date format: {e}")
        
        if end < start:
            return (False, "End date must be after start date")

        # Validación: la reserva debe hacerse con al menos 72 horas de antelación
        min_allowed_date = (datetime.now() + timedelta(hours=72)).date()
        if start.date() < min_allowed_date:
            return (False, f"Reservations must be made at least 72 hours in advance. Earliest start date: {min_allowed_date.strftime('%Y-%m-%d')}")
        
        # VALIDACIÓN DE EXCLUSIÓN MUTUA: Verificar si el usuario ya tiene otro hotel
        existing_hotel = self.has_overlapping_hotel_reservation(user, start, end)
        if existing_hotel:
            return (False, f"CONFLICT: You already have a hotel reservation from {existing_hotel.get('start')} to {existing_hotel.get('end')}. "
                          f"You cannot reserve two hotels at the same time (Mutual Exclusion Policy).")
        
        reservations = self.load_reservations()
        hotel_reservations = reservations.get('hotel_reservations', [])
        
        if not self.is_resource_available(hotel_name, room_type, start, end, room.get('count', 0), hotel_reservations):
            duration_days = (end - start).days or 1
            next_slot = self.find_next_available_slot(hotel_name, room_type, duration_days, 'hotel')
            if next_slot:
                return (False, f"No rooms available. Next available: {next_slot[0]} to {next_slot[1]}")
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
        self.save_reservations(reservations)
        
        return (True, json.dumps(entry, ensure_ascii=False, indent=2))
    
    def get_user_reservations(self, user: str) -> Tuple[List, List]:
        """Retorna las reservas del usuario separadas en vehículos y hoteles.

        Args:
            user: Nombre/identificador del usuario.

        Returns:
            Tuple (vehicle_list, hotel_list) filtradas por `user`.
        """
        reservations = self.load_reservations()
        vehicle = [r for r in reservations.get('vehicle_reservations', []) if r.get('user') == user]
        hotel = [r for r in reservations.get('hotel_reservations', []) if r.get('user') == user]
        return (vehicle, hotel)
    
    def cancel_reservation(self, res_id: str, res_type: str = 'vehicle') -> bool:
        """Cancela una reserva por su `id`.

        Args:
            res_id: Identificador de la reserva (se usa campo 'id').
            res_type: 'vehicle' o 'hotel' para elegir la lista a inspeccionar.

        Comportamiento:
            - Filtra la lista correspondiente para eliminar la reserva con `id` igual a `res_id`.
            - Si hubo un cambio, guarda el archivo y retorna True; en otro caso retorna False.
        """
        reservations = self.load_reservations()
        key = 'vehicle_reservations' if res_type == 'vehicle' else 'hotel_reservations'
        
        if key not in reservations:
            print(f"Error: Reservation type '{res_type}' not found")
            return False
        
        original_count = len(reservations[key])
        reservations[key] = [r for r in reservations[key] if r.get('id') != res_id]
        
        if len(reservations[key]) < original_count:
            if self.save_reservations(reservations):
                print(f"✓ Reservation cancelled successfully. ID: {res_id}")
                return True
            else:
                print("Error saving changes.")
                return False
        
        print(f"✗ No reservation found with ID: {res_id}")
        return False
