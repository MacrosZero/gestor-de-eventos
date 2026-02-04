# ARCHITECTURAL DOCUMENTATION - Sistema de Reservas OOP

**VERSIÓN:** 2.0 - Arquitectura Orientada a Objetos con Inyección de Dependencias  
**ESTADO:** Producción

---

## VISIÓN GENERAL DE LA ARQUITECTURA

El sistema ha sido restructurado completamente usando Programación Orientada a 
Objetos (OOP). Cada componente es una clase independiente que colabora con otras
a través de inyección de dependencias (Dependency Injection).

Este diseño permite:
- ✓ Bajo acoplamiento entre componentes
- ✓ Fácil testabilidad
- ✓ Migración a otras tecnologías (SQL, MongoDB, etc.)
- ✓ Reutilización de componentes
- ✓ Cumplimiento de SOLID

```
                    ┌─────────────────────────┐
                    │  ReservationApp         │
                    │  (ORQUESTADOR PRINCIPAL)│
                    └──────────┬──────────────┘
                               │
                ┌──────────────┼──────────────────┐
                │              │                  │
         ┌──────▼────────┐  ┌──▼──────────┐  ┌──▼──────────────────┐
         │ DatabaseMgr   │  │MenuManager  │  │ UserManager         │
         │ (Persistencia)│  │ (Interfaz)  │  │ ResourceManager     │
         └───────────────┘  └──────┬──────┘  │ ReservationManager  │
              ▲                     │         └──────────────────────┘
              │                     │
              └─────────────────────┘
              (Todas las clases usan DB)
```

---

## DESCRIPCIÓN DE CLASES

### 1. ReservationApp (app.py) - ORQUESTADOR

**Propósito:**
- Punto de entrada único de la aplicación
- Inicializa todos los componentes
- Orquesta el flujo general

**Responsabilidades:**
- Crear instancias de DatabaseManager
- Crear instancias de todos los Managers (UserMgr, ResourceMgr, etc.)
- Pasar dependencias inyectadas a cada Manager
- Iniciar el menú principal
- Manejar excepciones generales

**Métodos públicos:**
- `__init__(base_dir)` → Inicializa componentes
- `run()` → Inicia la aplicación

**Inyecciones de dependencia:**
- DatabaseManager → UserManager
- DatabaseManager → ResourceManager
- DatabaseManager → ReservationManager
- ResourceManager → ReservationManager
- UserManager → MenuManager
- ResourceManager → MenuManager
- ReservationManager → MenuManager

**Beneficio de este patrón:**
- Cambiar a otra BD solo modificando DatabaseManager y aquí

---

### 2. DatabaseManager (database.py) - CAPA DE PERSISTENCIA

**Propósito:**
- Abstrae TODAS las operaciones de entrada/salida con archivos JSON
- 100% agnóstico respecto a estructura de datos
- Fácil de extender a SQL, MongoDB, etc.

**Responsabilidades:**
- Resolver rutas de archivos
- Leer/escribir archivos JSON
- Manejo de errores de IO
- Encapsular formato de persistencia

**Métodos públicos:**
- `resolve_path(json_file)` → Convierte nombre en ruta absoluta
- `load(json_file, default)` → Carga JSON con default
- `save(json_file, data)` → Guarda JSON
- `load_json_file(json_file)` → Carga JSON exacto
- `save_json_file(json_file, data)` → Guarda JSON sin procesamiento

**Archivos manejados:**
- `login.json` → `{"users": [...]}` ← Responsabilidad de UserManager
- `res_data.json` → `{"hotels": [...], "cars": [...], "chofer": [...]}`
- `reservations.json` → `{"vehicle_reservations": [...], "hotel_reservations": [...]}`

> **IMPORTANTE:** DatabaseManager es completamente agnóstico.
> Cada Manager es responsable de preparar sus datos en la estructura correcta.

**Ejemplo de extensión a SQL:**
- Reemplazar `load_json_file()` → query() con SQLAlchemy
- Reemplazar `save_json_file()` → insert/update() con SQLAlchemy
- Todos los Managers seguirían funcionando sin cambios
- Solo modificas DatabaseManager

---

### 3. UserManager (user_manager.py) - GESTIÓN DE USUARIOS

**Propósito:**
- Gestionar autenticación, registro y roles de usuarios
- Mantener integridad de datos de usuarios

**Dependencias inyectadas:**
- DatabaseManager (para leer/escribir login.json)

**Responsabilidades:**
- Validar campos vacíos
- Verificar duplicados (username único)
- Hashear passwords (SHA256 + PBKDF2, 100k iteraciones)
- Gestionar estructura JSON `{"users": [...]}`
- Gestionar roles (admin/user)
- Autenticación segura

**Métodos públicos:**
- `register_user(username, password)` → Registra nuevo usuario
- `login(username, password)` → Autentica usuario
- `make_admin()` → Interactivo: promover a admin
- `display_user_data(username, role)` → Muestra perfil
- `get_all_users()` → Retorna todos usuarios

**Métodos privados (Gestión interna):**
- `_get_users()` → Extrae usuarios desde `{"users": [...]}`
- `_save_users(users)` → Prepara y guarda formato `{"users": [...]}`
- `_hash_password(password)` → SHA256 + PBKDF2
- `_verify_password(password, hash)` → Verifica hash

**Estructura de datos:**
- En JSON: `{"users": [{"username": "", "password": "hash", "role": "user/admin"}]}`
- En memoria: lista de dicts con username, password, role
- El Manager es responsable de la conversión

**Validaciones:**
- Username no vacío y máx 50 chars
- Password no vacío y mínimo 6 chars (futuro mejorar)
- Username único (case-insensitive)
- Role solo "user" o "admin"

---

### 4. ResourceManager (resource_manager.py) - GESTIÓN DE RECURSOS

**Propósito:**
- Gestionar hoteles, vehículos y choferes
- Mantener inventario disponible

**Dependencias inyectadas:**
- DatabaseManager (para leer/escribir res_data.json)

**Responsabilidades:**
- Cargar/guardar estructura JSON de recursos
- CRUD de hoteles, autos, choferes
- Validar datos de entrada
- Mantener integridad de inventario
- Mostrar información formateada

**Métodos públicos:**

**OPERACIONES GENERALES:**
- `load_resources()` → Carga todas las categorías
- `save_resources(data)` → Guarda todas las categorías
- `load_resource_type(type)` → Obtiene lista de un tipo

**HOTELES:**
- `add_hotel()` → Interactivo: agrega hotel
- `get_hotel(hotel_name)` → Obtiene un hotel específico
- `get_all_hotels()` → Retorna todos hoteles

**VEHÍCULOS:**
- `add_car()` → Interactivo: agrega/actualiza coche
- `get_car(car_type)` → Obtiene tipo de coche
- `get_available_cars()` → Solo coches con count > 0
- `get_all_cars()` → Todos los coches
- `update_car_availability()` → Decrementa unidades (usado por ReservationMgr)

**CHOFERES:**
- `add_driver()` → Interactivo: agrega chofer
- `get_all_drivers()` → Retorna todos choferes
- `find_driver_by_license(type)` → Busca chofer por licencia

**VISUALIZACIÓN:**
- `show_resources_summary()` → Resumen de todos
- `show_resource_type(res_type)` → Detalle de un tipo

**Estructura de datos (res_data.json):**
```json
{
  "hotels": [
    {"name": "Hotel A", "location": "City", "rooms": 50, "price": 100}
  ],
  "cars": [
    {"type": "Toyota Camry", "count": 5}
  ],
  "chofer": [
    {"name": "Juan", "license": "Commercial"}
  ]
}
```

**Validaciones:**
- Hotel: nombre y ubicación no vacíos
- Auto: tipo no vacío, count > 0
- Chofer: nombre y licencia no vacíos

---

### 5. ReservationManager (reservation_manager.py) - GESTIÓN DE RESERVAS

**Propósito:**
- Gestionar reservas de vehículos y hoteles
- Verificar disponibilidad
- Evitar solapamiento de reservas

**Dependencias inyectadas:**
- DatabaseManager (para leer/escribir reservations.json)
- ResourceManager (para verificar disponibilidad de recursos)

**Responsabilidades:**
- Crear reservas con ID único (timestamp)
- Verificar disponibilidad sin solapamiento
- Sugerir próximo slot disponible
- Gestionar dos tipos de reservas (vehículos y hoteles)
- Cancelar reservas por ID
- Validar fechas
- Asegurar que unidades se decrementan

**Métodos públicos:**

**UTILIDADES:**
- `load_reservations()` → Carga todas
- `save_reservations(data)` → Guarda todas
- `parse_date(date_str)` → Parsea 'YYYY-MM-DD' o ISO
- `find_next_available_slot(...)` → Busca próximo slot

**RESERVAS DE VEHÍCULOS:**
- `rent_vehicle(user, car_type, start, end, need_driver)`
  - Verificar disponibilidad del coche
  - Si necesita chofer, verificar disponibilidad
  - Crear reserva con ID único
  - Guardar en vehicle_reservations
  - Actualizar contador de autos en ResourceManager
  - Retorna: (True, "Reserva exitosa") o (False, "Motivo del error")

**RESERVAS DE HOTELES:**
- `reserve_hotel(user, hotel, room, start, end, pax)`
  - Verificar disponibilidad de habitación
  - Crear reserva con ID único
  - Guardar en hotel_reservations
  - Retorna: (True, "Reserva exitosa") o (False, "Motivo del error")

**CONSULTAS:**
- `is_resource_available(...)` → Verifica disponibilidad exacta
- `get_user_reservations(user)` → Obtiene reservas usuario
- `cancel_reservation(res_id, res_type)` → Cancela por ID

**Características avanzadas:**
- ID único usando timestamp + microsegundos
- Detección de solapamiento: if (start_req < res_end) and (res_start < end_req)
- Sugerencia de próximo slot disponible después de un rechazo
- Validación de fechas: start < end, fechas futuras, etc.
- Gestión de choferes: disponibilidad independiente
- Atomic operations: no hay reservas parciales

**Estructura de datos (reservations.json):**
```json
{
  "vehicle_reservations": [
    {
      "id": "1234567890.123456",
      "user": "testuser",
      "car_type": "Toyota Camry",
      "start": "2026-02-05",
      "end": "2026-02-10",
      "need_driver": true,
      "driver": "Juan",
      "created_at": "2026-02-04T10:30:00"
    }
  ],
  "hotel_reservations": [
    {
      "id": "1234567890.654321",
      "user": "testuser",
      "hotel": "Hotel A",
      "room_type": "Standard",
      "start": "2026-02-05",
      "end": "2026-02-10",
      "guests": 2,
      "created_at": "2026-02-04T10:30:00"
    }
  ]
}
```

**Manejo de errores:**
- Fecha inválida → (False, "Invalid date format")
- Recurso no existe → (False, "Resource not found")
- No hay disponibilidad → (False, "Not available. Next available: ...")
- Chofer no existe → (False, "Driver not found")

---

### 6. MenuManager (menu_manager.py) - INTERFAZ DE USUARIO

**Propósito:**
- Presentar menús interactivos
- Orquestar flujo de interacción con usuario
- Traducir opciones del usuario en llamadas a los Managers

**Dependencias inyectadas:**
- UserManager
- ResourceManager
- ReservationManager

**Responsabilidades:**
- Mostrar opciones de menú
- Capturar input del usuario
- Validar opciones seleccionadas
- Llamar métodos apropiados de otros Managers
- Formatear y mostrar resultados
- Manejar navegación entre menús

**Menús públicos:**
- `main_menu()` → Menú inicial (Register/Login/Exit)
- `admin_menu(username, role)` → Menú de administrador
- `user_menu(username, role)` → Menú de usuario normal

**Menús internos (privados):**
- `_manage_resources_menu()` → Add Hotel/Car/Driver
- `_view_resources_menu()` → Ver recursos por tipo
- `_rent_vehicle_cli(user)` → Interfaz de renta de vehículos
- `_reserve_hotel_cli(user)` → Interfaz de reserva de hotel
- `_view_user_reservations()` → Ver mis reservas
- `_cancel_reservation_cli()` → Cancelar reserva

**Flujo típico:**
- main_menu() → selecciona "1. Register" → register_user()
- main_menu() → selecciona "2. Login" → login()
- Si es admin:
  - admin_menu() → gestionar recursos/usuarios
- Si es user:
  - user_menu() → rentar/reservar/ver reservas
- logout() vuelve a main_menu()

**Responsabilidad:** MenuManager NO hace lógica de negocio,
solo orquesta llamadas y formatea output.

---

## PATRONES DE DISEÑO APLICADOS

### 1. INYECCIÓN DE DEPENDENCIAS (Dependency Injection)

**Beneficios:**
- Bajo acoplamiento entre componentes
- Fácil de testear (mockear dependencias)
- Fácil de cambiar implementaciones
- Responsabilidades claras

**Ejemplo en el código:**
```python
class UserManager:
    def __init__(self, db: DatabaseManager):
        self.db = db  # ← Inyección de DatabaseManager
```

**Ventaja:** Cambiar a otra BD solo modificando DatabaseManager

---

### 2. PRINCIPIO DE RESPONSABILIDAD ÚNICA (SRP)

Cada clase tiene UNA responsabilidad:
- DatabaseManager → Persistencia
- UserManager → Usuarios
- ResourceManager → Recursos
- ReservationManager → Reservas
- MenuManager → Interfaz
- ReservationApp → Orquestación

**Beneficios:**
- Código más legible
- Menos bugs (cambios no afectan otros)
- Fácil testear
- Fácil reutilizar

---

### 3. PATRÓN STRATEGY (para persistencia)

DatabaseManager implementa una "estrategia" de persistencia (JSON actual).

Para cambiar a SQL:
- Crear SQLDatabaseManager que implemente la misma interfaz
- Cambiar solo la línea de inyección en ReservationApp
- Todos los Managers funcionan sin cambios

**Interfaz esperada:**
- `load_json_file(filename)` → Dict/List
- `save_json_file(filename, data)` → bool
- `resolve_path(filename)` → str

---

## FLUJO DE DATOS Y CONTROL

### Ejemplo: Usuario registra y hace una reserva

1. **Usuario ejecuta:** `python app.py`
   - ReservationApp.__init__() crea todas las instancias
   - ReservationApp.run() → MenuManager.main_menu()

2. **Usuario selecciona "1. Register"**
   - MenuManager pide username/password
   - MenuManager llama: UserManager.register_user(username, password)
   - UserManager valida y hashea password
   - UserManager llama: DatabaseManager.load("login.json", {})
   - UserManager modifica estructura {"users": [...]}
   - UserManager llama: DatabaseManager.save("login.json", data)
   - DatabaseManager.save_json_file() escribe el archivo

3. **Usuario selecciona "2. Login"**
   - MenuManager pide username/password
   - MenuManager llama: UserManager.login(username, password)
   - UserManager verifica credenciales
   - Si es admin: MenuManager.admin_menu()
   - Si es user: MenuManager.user_menu()

4. **Usuario elige "Rent Vehicle"**
   - MenuManager pide car_type, dates, need_driver
   - MenuManager llama: ReservationManager.rent_vehicle(...)
   - ReservationManager verifica disponibilidad:
     - Llama: ResourceManager.get_car(car_type)
     - Llama: ReservationManager.is_resource_available(...)
       - Lee reservations.json vía DatabaseManager
       - Busca solapamientos
   - Si disponible:
     - Crea reserva con ID único
     - Llamar: ResourceManager.update_car_availability()
     - Guardar: DatabaseManager.save_json_file("reservations.json", ...)
   - Retorna (True, message) o (False, reason)

5. **Usuario hace logout**
   - MenuManager vuelve a main_menu()

---

## PATRONES AVANZADOS: EXTENSIBILIDAD FUTURA

### 1. AGREGAR API REST

```python
from flask import Flask
from app import ReservationApp

app = ReservationApp()
flask_app = Flask(__name__)

@flask_app.route('/users/register', methods=['POST'])
def register():
    data = request.json
    success = app.user_mgr.register_user(data['username'], data['password'])
    return {"success": success}
```

✓ Todos los Managers funcionan sin cambios
✓ Solo creas endpoints que llaman a los Managers

---

### 2. CAMBIAR A SQL

```python
class SQLDatabaseManager(DatabaseManager):
    def load_json_file(self, filename):
        # Implementar query SQL
        pass
    
    def save_json_file(self, filename, data):
        # Implementar insert/update SQL
        pass

# En ReservationApp:
self.db = SQLDatabaseManager()  # ← Un cambio
# Todos los Managers funcionan igual
```

---

### 3. AGREGAR CACHE

```python
class CachedDatabaseManager(DatabaseManager):
    def __init__(self):
        self.cache = {}
    
    def load_json_file(self, filename):
        if filename in self.cache:
            return self.cache[filename]
        data = super().load_json_file(filename)
        self.cache[filename] = data
        return data
```

---

### 4. AGREGAR LOGGING

```python
@log_calls
class UserManager:
    # Automáticamente loguea cada método
    pass
```

---

### 5. AGREGAR NOTIFICACIONES

```python
class NotificationManager:
    def on_reservation_created(self, reservation):
        send_email(user, "Tu reserva fue creada")

# En ReservationManager:
self.notification_mgr.on_reservation_created(...)
```

---

## CONCLUSIÓN Y BENEFICIOS ARQUITECTÓNICOS

- ✓ **BAJO ACOPLAMIENTO** → Cambiar una clase no afecta otras
- ✓ **ALTA COHESIÓN** → Cada clase agrupa funcionalidad relacionada
- ✓ **REUTILIZABLE** → Los Managers se pueden usar en cualquier contexto (CLI, API, GUI)
- ✓ **TESTEABLE** → Mock DatabaseManager para tests unitarios
- ✓ **MANTENIBLE** → Código organizado y responsabilidades claras
- ✓ **ESCALABLE** → Fácil agregar API, cambiar BD, agregar features
- ✓ **PROFESIONAL** → Sigue SOLID, estándares Python, buenas prácticas
- ✓ **DOCUMENTADO** → Código auto-documentado con docstrings
