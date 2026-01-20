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
        """Carga todas las reservas"""
        data = self.db.load_json_file(self.reservations_file)
        if not data:
            return {"vehicle_reservations": [], "hotel_reservations": []}
        return data
    
    def save_reservations(self, reservations: Dict) -> bool:
        """Guarda todas las reservas"""
        return self.db.save_json_file(self.reservations_file, reservations)
    
    def parse_date(self, date_str: str) -> datetime:
        """Parsea fecha en 'YYYY-MM-DD' o formato ISO"""
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return datetime.fromisoformat(date_str)
    
    def is_resource_available(self, resource_name: str, resource_type: str, 
                            start_req: datetime, end_req: datetime, 
                            total_inventory: int, reservations_list: List) -> bool:
        """Verifica si un recurso está disponible en un rango de fechas"""
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
        """
        Verifica si un usuario ya tiene una reserva de vehículo que se solapa con las fechas solicitadas.
        Restricción de Exclusión Mutua: No puede haber dos vehículos reservados simultáneamente.
        
        Args:
            user: Nombre del usuario
            start_req: Fecha de inicio solicitada
            end_req: Fecha de fin solicitada
            
        Returns:
            Dict con la reserva existente si hay conflicto, None si está disponible
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
        """
        Verifica si un usuario ya tiene una reserva de hotel que se solapa con las fechas solicitadas.
        Restricción de Exclusión Mutua: No puede haber dos hoteles reservados simultáneamente.
        
        Args:
            user: Nombre del usuario
            start_req: Fecha de inicio solicitada
            end_req: Fecha de fin solicitada
            
        Returns:
            Dict con la reserva existente si hay conflicto, None si está disponible
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
        """Encuentra el próximo slot disponible para un recurso"""
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
        """
        Reserva un vehículo.
        
        Validaciones:
        - El recurso debe existir
        - Las fechas deben ser válidas
        - El recurso debe estar disponible
        - EXCLUSIÓN MUTUA: El usuario no puede tener otro vehículo en esas fechas
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
        """
        Reserva una habitación de hotel.
        
        Validaciones:
        - El hotel debe existir
        - La habitación debe existir
        - Las fechas deben ser válidas
        - La habitación debe estar disponible
        - EXCLUSIÓN MUTUA: El usuario no puede tener otro hotel en esas fechas
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
        """Obtiene las reservas de un usuario"""
        reservations = self.load_reservations()
        vehicle = [r for r in reservations.get('vehicle_reservations', []) if r.get('user') == user]
        hotel = [r for r in reservations.get('hotel_reservations', []) if r.get('user') == user]
        return (vehicle, hotel)
    
    def cancel_reservation(self, res_id: str, res_type: str = 'vehicle') -> bool:
        """Cancela una reservación por su ID"""
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
