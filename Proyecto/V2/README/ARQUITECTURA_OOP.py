"""
ARCHITECTURAL DOCUMENTATION - Sistema de Reservas OOP

================================================================================
VISIÓN GENERAL DE LA ARQUITECTURA
================================================================================

El sistema ha sido restructurado completamente usando Programación Orientada a 
Objetos (OOP). Cada componente es una clase independiente que colabora con otras
a través de inyección de dependencias.

                    ┌─────────────────────┐
                    │  ReservationApp     │
                    │  (MAIN/ORQUESTADOR) │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
         ┌──────▼────────┐  ┌──▼──────────┐  └────────────────┐
         │ DatabaseMgr   │  │MenuManager  │                   │
         │               │  │             │          ┌────────▼──────────┐
         └───────────────┘  └──────┬──────┘          │ UserManager       │
              ▲                     │                │ ResourceManager   │
              │                     │                │ ReservationManager│
              └─────────────────────┼────────────────┴────────────────────┘
                                    │
                         ┌──────────▼─────────────┐
                         │ Flujo de Usuario       │
                         └────────────────────────┘

================================================================================
DESCRIPCIÓN DE CLASES
================================================================================

1. DatabaseManager (database.py)
   ════════════════════════════════
   
   Propósito: Abstrae todas las operaciones de entrada/salida con archivos JSON
              (100% agnóstico respecto a estructura de datos)
   
   Métodos públicos:
   ├─ __init__(base_dir)              → Inicializa con directorio base
   ├─ resolve_path(json_file)         → Convierte nombre en ruta absoluta
   ├─ load(json_file, default)        → Carga datos, delega a load_json_file()
   ├─ save(json_file, data)           → Guarda datos, delega a save_json_file()
   ├─ load_json_file(json_file)       → Carga JSON exacto del archivo
   └─ save_json_file(json_file, data) → Guarda JSON sin procesamiento
   
   Archivos manejados:
   ├─ login.json        (estructura: {"users": [...]}) ← UserManager responsable
   ├─ res_data          (estructura: {hotels, cars, chofer})
   └─ reservations.json (estructura: {vehicle_reservations, hotel_reservations})
   
   NOTA: DatabaseManager es completamente agnóstico. Cada Manager es responsable
         de preparar sus datos en la estructura correcta antes de guardar.
   
   Ventaja: Cambiar BD a MongoDB/SQL solo modificando esta clase


2. UserManager (user_manager.py)
   ═════════════════════════════════
   
   Propósito: Gestionar autenticación, registro y roles de usuarios
   
   Métodos públicos:
   ├─ register_user(username, password)              → Registra nuevo usuario
   ├─ login(username, password)                      → Autentica usuario
   ├─ make_admin(username)                           → Promueve a admin
   ├─ display_user_data(username, role)              → Muestra perfil
   ├─ get_all_users()                                → Retorna todos usuarios
   
   Métodos privados (Gestión de formato JSON):
   ├─ _get_users()                                   → Extrae usuarios desde {"users": [...]}
   └─ _save_users(users)                             → Prepara y guarda formato {"users": [...]}
   
   Responsabilidades:
   ├─ Validar campos vacíos
   ├─ Verificar duplicados
   ├─ Gestionar estructura JSON de usuarios
   ├─ Encriptar passwords (futuro)
   └─ Gestionar roles (admin/user)


3. ResourceManager (resource_manager.py)
   ════════════════════════════════════════
   
   Propósito: Gestionar hoteles, autos y choferes
   
   Métodos públicos:
   
   HOTELES:
   ├─ add_hotel()                    → Interactivo: agrega hotel
   ├─ get_hotel(hotel_name)          → Obtiene un hotel
   └─ get_all_hotels()               → Retorna todos hoteles
   
   AUTOS:
   ├─ add_car()                      → Interactivo: agrega/actualiza coche
   ├─ get_car(car_type)              → Obtiene tipo de coche
   ├─ get_available_cars()           → Solo disponibles (count > 0)
   └─ get_all_cars()                 → Todos los coches
   
   CHOFERES:
   ├─ add_driver()                   → Interactivo: agrega chofer
   ├─ get_all_drivers()              → Retorna todos choferes
   └─ find_driver_by_license(type)   → Busca por tipo de licencia
   
   VISUALIZACIÓN:
   ├─ show_resources_summary()       → Resumen de todos
   └─ show_resource_type(res_type)   → Detalle de un tipo


4. ReservationManager (reservation_manager.py)
   ═════════════════════════════════════════════
   
   Propósito: Gestionar reservas de vehículos y hoteles
   
   Métodos públicos:
   
   UTILIDADES:
   ├─ load_reservations()                           → Carga todas las reservas
   ├─ save_reservations(data)                       → Guarda reservas
   ├─ parse_date(date_str)                          → Parsea fecha
   └─ find_next_available_slot(...)                 → Busca próximo slot
   
   RESERVAS:
   ├─ rent_vehicle(user, car_type, start, end, need_driver)
   ├─ reserve_hotel(user, hotel, room, start, end, pax)
   ├─ is_resource_available(...)                    → Verifica disponibilidad
   ├─ get_user_reservations(user)                   → Obtiene reservas usuario
   └─ cancel_reservation(res_id, res_type)          → Cancela por ID
   
   Características:
   ├─ ID único usando timestamp (created_at)
   ├─ Manejo de disponibilidad (sin solapamiento)
   ├─ Sugerencia de próxima disponibilidad
   └─ Validación de fechas


5. MenuManager (menu_manager.py)
   ═══════════════════════════════
   
   Propósito: Gestionar interfaces CLI y flujos de usuario
   
   Menús públicos:
   ├─ main_menu()                   → Menú principal (Register/Login/Exit)
   ├─ admin_menu(username, role)    → Menú de administrador
   └─ user_menu(username, role)     → Menú de usuario normal
   
   Menús internos (privados):
   ├─ _manage_resources_menu()      → Add Hotel/Car/Driver
   ├─ _view_resources_menu()        → Ver recursos
   ├─ _rent_vehicle_cli()           → Interfaz para reservar vehículo
   ├─ _reserve_hotel_cli()          → Interfaz para reservar hotel
   ├─ _view_user_reservations()     → Mostrar reservas del usuario
   └─ _cancel_reservation_cli()     → Interfaz para cancelar
   
   Características:
   ├─ Flujos interactivos con input()
   ├─ Validación de opciones
   ├─ Manejo de errores
   └─ Mensajes visuales con símbolos (✓ ✗)


6. ReservationApp (app.py)
   ═════════════════════════
   
   Propósito: Orquestar toda la aplicación
   
   Métodos:
   ├─ __init__(base_dir)            → Inicializa todas las clases
   ├─ run()                          → Inicia el menú principal
   └─ main()                         → Punto de entrada
   
   Responsabilidades:
   ├─ Crear instancias de todas las clases
   ├─ Inyectar dependencias
   ├─ Capturar excepciones
   └─ Mostrar interfaz inicial


================================================================================
FLUJO DE DEPENDENCIAS
================================================================================

app.py (main)
    │
    ├─> DatabaseManager()           (sin dependencias)
    │
    ├─> UserManager(db)             (depende de DatabaseManager)
    │
    ├─> ResourceManager(db)         (depende de DatabaseManager)
    │
    ├─> ReservationManager(db, resource_mgr)  (depende de DatabaseManager y ResourceManager)
    │
    └─> MenuManager(user_mgr, resource_mgr, reservation_mgr)
        (depende de las tres clases anteriores)


================================================================================
PATRONES DE DISEÑO UTILIZADOS
================================================================================

1. Singleton Pattern (implícito):
   - Una sola instancia de cada manager durante la ejecución

2. Dependency Injection:
   - Cada clase recibe sus dependencias en __init__
   - Facilita pruebas unitarias y cambios

3. Abstraction:
   - DatabaseManager abstrae los detalles de persistencia
   - MenuManager abstrae la interfaz CLI

4. Separation of Concerns:
   - Cada clase tiene responsabilidad única
   - Los cambios en una no afectan otras

5. Factory Pattern (implícito):
   - ReservationApp actúa como factory creando todas las instancias


================================================================================
CÓMO EJECUTAR
================================================================================

Opción 1: Directamente (RECOMENDADO)
    python c:\Estudio\Deving\Proyecto\V2\app\app.py

Opción 2: Con __main__.py
    python -m V2.app

Opción 3: Importar como módulo
    from V2.app.app import ReservationApp
    app = ReservationApp()
    app.run()


================================================================================
EXTENSIBILIDAD FUTURA
================================================================================

Agregar base de datos SQL:
    └─ Ver: c:\Estudio\Deving\Proyecto\V2\app\database.py
    └─ Crear SQLDatabaseManager(DatabaseManager)
    └─ Cambiar en c:\Estudio\Deving\Proyecto\V2\app\app.py:
       self.db = SQLDatabaseManager()

Agregar API REST:
    └─ Crear APIManager que use los managers existentes
    └─ Reutiliza toda la lógica

Agregar GUI:
    └─ Crear GUIManager en lugar de MenuManager
    └─ Reutiliza todos los managers

Agregar autenticación JWT:
    └─ Extender UserManager
    └─ Sin tocar otras clases


================================================================================
BENEFICIOS FINALES
================================================================================

✓ Código modular y mantenible
✓ Fácil de probar cada componente
✓ Reutilizable en otros proyectos
✓ Escalable a nuevas funcionalidades
✓ Bajo acoplamiento entre clases
✓ Alto nivel de cohesión
✓ Sigue principios SOLID
✓ Profesional y enterprise-ready

================================================================================
"""
