"""
Resource Manager - Gestiona recursos (hoteles, autos, choferes)
"""
from database import DatabaseManager
from typing import List, Dict, Optional


class ResourceManager:
    """Gestiona hoteles, autos y choferes"""
    
    def __init__(self, db: DatabaseManager):
        """Inicializa el gestor de recursos.

        Args:
            db: Instancia de `DatabaseManager` usada para leer/escribir
                los archivos JSON de recursos.

        Notas:
            - No realiza IO adicional al inicializar; solo guarda la referencia
              al gestor de base de datos.
            - `res_file` define el nombre del archivo JSON (usado por
              `load_resources` / `save_resources`).
        """
        self.db = db
        self.res_file = "res_data.json"
    
    def load_resources(self) -> Dict:
        """Carga y retorna el contenido del archivo de recursos.

        Returns:
            Dict con la estructura completa de recursos (hotels, cars, chofer, ...).

        Efectos secundarios:
            - Lee desde el archivo definido en `self.res_file` usando
              `DatabaseManager.load_json_file`.
            - Si el archivo no existe devuelve un diccionario vacío.
        """
        return self.db.load_json_file(self.res_file)
    
    def save_resources(self, data: Dict) -> bool:
        """Guarda la estructura de recursos pasada en el archivo definido.

        Args:
            data: Diccionario con la estructura de recursos que será serializada
                  a JSON.

        Returns:
            True si el guardado fue exitoso, False en caso de error de IO.
        """
        return self.db.save_json_file(self.res_file, data)
    
    def load_resource_type(self, res_type: str) -> List:
        """Devuelve la lista para un tipo de recurso concreto.

        Args:
            res_type: Nombre de la clave en el JSON (por ejemplo 'cars', 'hotels', 'chofer').

        Returns:
            Lista asociada a `res_type` o lista vacía si no existe.
        """
        data = self.load_resources()
        return data.get(res_type, [])
    
    # ============== HOTELES ==============
    
    def add_hotel(self) -> bool:
        """Añade un nuevo hotel pidiendo datos por consola.

        Flujo:
            - Solicita `name`, `location` y números de habitaciones y precio.
            - Valida entradas numéricas (devuelve False si hay error).
            - Añade el nuevo hotel a la lista `hotels` en el JSON y guarda.

        Returns:
            True si el hotel fue agregado y guardado exitosamente, False en caso contrario.
        """
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
        """Busca y retorna el diccionario del hotel cuyo nombre coincide (case-insensitive).

        Args:
            hotel_name: Nombre del hotel a buscar.

        Returns:
            Diccionario del hotel si existe, None en caso contrario.
        """
        hotels = self.load_resource_type("hotels")
        return next((h for h in hotels if h.get('name', '').lower() == hotel_name.lower()), None)
    
    def get_all_hotels(self) -> List[Dict]:
        """Retorna la lista completa de hoteles.

        Nota: siempre devuelve una lista (vacía si no hay hoteles).
        """
        return self.load_resource_type("hotels")
    
    # ============== AUTOS ==============
    
    def add_car(self) -> bool:
        """Añade o actualiza un tipo de coche mediante entrada interactiva.

        Comportamiento:
            - Lee `car_type` y cantidad `qty` (positivo para añadir, negativo para restar).
            - Si el tipo existe actualiza `count` (sin bajar de 0) y guarda.
            - Si no existe, pregunta si crear nuevo registro y solicita precio, asientos y licencia.
            - Usa `data.setdefault('cars', [])` al crear un nuevo tipo para evitar KeyError.

        Returns:
            True si la operación se completó y los datos fueron guardados, False si hubo error.
        """
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
        """Busca y retorna un dict para el tipo de coche solicitado (case-insensitive).

        Args:
            car_type: Tipo de coche (por ejemplo 'sedan', 'van', 'motorcycle').

        Returns:
            Diccionario del coche si existe, None en caso contrario.
        """
        cars = self.load_resource_type("cars")
        return next((c for c in cars if c.get('type', '').lower() == car_type.lower()), None)
    
    def get_available_cars(self) -> List[Dict]:
        """Retorna la lista de coches cuyo `count` es mayor que 0.

        Uso típico: mostrar opciones al usuario antes de reservar.
        """
        cars = self.load_resource_type("cars")
        return [c for c in cars if c.get('count', 0) > 0]
    
    def get_all_cars(self) -> List[Dict]:
        """Retorna la lista completa de coches (incluye count = 0).

        Nota: útil para inspección administrativa.
        """
        return self.load_resource_type("cars")
    
    # ============== CHOFERES ==============
    
    def add_driver(self) -> bool:
        """Añade un nuevo chofer pidiendo datos por consola.

        Validaciones:
            - Todos los campos (`name`, `license_type`, `CI`) son obligatorios.
            - Guarda en la clave `chofer` del JSON.

        Returns:
            True si el chofer fue agregado y guardado correctamente, False si faltan campos o hay error.
        """
        name = input("Driver name: ").strip()
        license_type = input("License type: ").strip()
        ci = input("CI: ").strip()
        
        if len(ci) != 11:
            print("Error: CI must be exactly 11 characters.")
            return False

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
        """Retorna la lista de choferes (puede ser vacía).

        Nota: lee la clave `chofer` del archivo de recursos.
        """
        return self.load_resource_type("chofer")
    
    def find_driver_by_license(self, license_type: str) -> Optional[Dict]:
        """Busca y retorna el primer chofer que tenga el `license_type` solicitado.

        Args:
            license_type: Tipo de licencia requerido (por ejemplo 'B').

        Returns:
            Diccionario del chofer disponible que coincida, o None si ninguno cumple.
        """
        drivers = self.get_all_drivers()
        return next((d for d in drivers if d.get('license_type', '').upper() == str(license_type).upper()), None)
    
    # ============== VISUALIZACIÓN ==============
    
    def show_resources_summary(self) -> None:
        """Imprime por consola un resumen de las claves presentes en el archivo de recursos.

        Formato: para cada clave del JSON se imprime el número de items (o 'N/A' si no aplica).
        Uso: utilidad administrativa/diagnóstica.
        """
        data = self.load_resources()
        print("\n--- Resources Summary ---")
        for key, value in data.items():
            try:
                length = len(value)
            except Exception:
                length = 'N/A'
            print(f"  {key}: {length} item(s)")
    
    def show_resource_type(self, res_type: str) -> None:
        """Imprime por consola los elementos de un tipo de recurso específico.

        Args:
            res_type: Clave a mostrar (por ejemplo 'hotels', 'cars', 'chofer').

        Comportamiento:
            - Si la lista está vacía informa que no hay recursos de ese tipo.
            - Para diccionarios anidados muestra sublistas y pares clave:valor.
        """
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
