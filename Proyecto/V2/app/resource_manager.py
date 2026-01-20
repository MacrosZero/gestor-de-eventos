"""
Resource Manager - Gestiona recursos (hoteles, autos, choferes)
"""
from database import DatabaseManager
from typing import List, Dict, Optional


class ResourceManager:
    """Gestiona hoteles, autos y choferes"""
    
    def __init__(self, db: DatabaseManager):
        """
        Inicializa el gestor de recursos.
        
        Args:
            db: Instancia de DatabaseManager
        """
        self.db = db
        self.res_file = "res_data.json"
    
    def load_resources(self) -> Dict:
        """Carga todos los recursos"""
        return self.db.load_json_file(self.res_file)
    
    def save_resources(self, data: Dict) -> bool:
        """Guarda todos los recursos"""
        return self.db.save_json_file(self.res_file, data)
    
    def load_resource_type(self, res_type: str) -> List:
        """Carga un tipo específico de recurso"""
        data = self.load_resources()
        return data.get(res_type, [])
    
    # ============== HOTELES ==============
    
    def add_hotel(self) -> bool:
        """Añade un nuevo hotel interactivamente"""
        name = input("Hotel name: ").strip()
        location = input("Hotel location: ").strip()
        
        try:
            single_room = int(input("Single rooms: "))
            double_room = int(input("Double rooms: "))
            triple_room = int(input("Triple rooms: "))
            price = int(input("Price per pax: "))
        except ValueError:
            print("Error: Invalid numeric input.")
            return False
        
        hotel = {
            "name": name,
            "location": location,
            "room": [
                {"type": "Single", "count": single_room, "pax": 1},
                {"type": "Double", "count": double_room, "pax": 2},
                {"type": "Triple", "count": triple_room, "pax": 3}
            ],
            "pax_price": price
        }
        
        data = self.load_resources()
        data.setdefault("hotels", []).append(hotel)
        
        if self.save_resources(data):
            print("Hotel added successfully.")
            return True
        return False
    
    def get_hotel(self, hotel_name: str) -> Optional[Dict]:
        """Obtiene un hotel por nombre"""
        hotels = self.load_resource_type("hotels")
        return next((h for h in hotels if h.get('name', '').lower() == hotel_name.lower()), None)
    
    def get_all_hotels(self) -> List[Dict]:
        """Retorna todos los hoteles"""
        return self.load_resource_type("hotels")
    
    # ============== AUTOS ==============
    
    def add_car(self) -> bool:
        """Añade o actualiza un tipo de coche"""
        car_type = input("Car type (sedan/van/bus/motorcycle): ").strip().lower()
        
        try:
            qty = int(input("Number of cars to add (negative to subtract): "))
        except ValueError:
            print("Error: Invalid number entered.")
            return False
        
        data = self.load_resources()
        cars = data.get("cars", [])
        
        # Buscar si el tipo de coche ya existe
        for car in cars:
            if car.get("type", "").lower() == car_type:
                old = car.get("count", 0)
                car["count"] = max(0, old + qty)
                self.save_resources(data)
                print(f"Updated '{car_type}' count: {old} -> {car['count']}")
                return True
        
        # Si no existe, ofrecer crearlo
        create = input(f"Car type '{car_type}' not found. Create new entry? (y/n): ").strip().lower()
        if create == 'y':
            try:
                price_per_day = int(input("Price per day: "))
                seats = int(input("Number of seats: "))
                license_type = input("License type: ").strip()
            except ValueError:
                print("Error: Invalid numeric input.")
                return False
            
            new_car = {
                "type": car_type,
                "price_per_day": price_per_day,
                "seats": seats,
                "count": max(0, qty),
                "licence_type": license_type
            }
            data.setdefault("cars", []).append(new_car)
            self.save_resources(data)
            print(f"Created new car type '{car_type}' with count {new_car['count']}")
            return True
        
        return False
    
    def get_car(self, car_type: str) -> Optional[Dict]:
        """Obtiene un tipo de coche por nombre"""
        cars = self.load_resource_type("cars")
        return next((c for c in cars if c.get('type', '').lower() == car_type.lower()), None)
    
    def get_available_cars(self) -> List[Dict]:
        """Retorna solo autos disponibles (count > 0)"""
        cars = self.load_resource_type("cars")
        return [c for c in cars if c.get('count', 0) > 0]
    
    def get_all_cars(self) -> List[Dict]:
        """Retorna todos los autos"""
        return self.load_resource_type("cars")
    
    # ============== CHOFERES ==============
    
    def add_driver(self) -> bool:
        """Añade un nuevo chofer interactivamente"""
        name = input("Driver name: ").strip()
        license_type = input("License type: ").strip()
        ci = input("CI: ").strip()
        
        if not all([name, license_type, ci]):
            print("Error: All fields are required.")
            return False
        
        driver = {"name": name, "license_type": license_type, "CI": ci}
        
        data = self.load_resources()
        data.setdefault("chofer", []).append(driver)
        
        if self.save_resources(data):
            print("Driver added successfully.")
            return True
        return False
    
    def get_all_drivers(self) -> List[Dict]:
        """Retorna todos los choferes"""
        return self.load_resource_type("chofer")
    
    def find_driver_by_license(self, license_type: str) -> Optional[Dict]:
        """Busca un chofer por tipo de licencia"""
        drivers = self.get_all_drivers()
        return next((d for d in drivers if d.get('license_type', '').upper() == str(license_type).upper()), None)
    
    # ============== VISUALIZACIÓN ==============
    
    def show_resources_summary(self) -> None:
        """Muestra resumen de todos los recursos"""
        data = self.load_resources()
        print("\n--- Resources Summary ---")
        for key, value in data.items():
            try:
                length = len(value)
            except Exception:
                length = 'N/A'
            print(f"  {key}: {length} item(s)")
    
    def show_resource_type(self, res_type: str) -> None:
        """Muestra recursos de un tipo específico"""
        res = self.load_resource_type(res_type)
        
        if not res:
            print(f"No resource '{res_type}' found or it's empty.")
            return
        
        print(f"\n--- {res_type.capitalize()} ---")
        
        if isinstance(res, list):
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
