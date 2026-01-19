"""
QUICK START - Guía rápida para probar el sistema
"""

# ============================================================================
# OPCIÓN 1: Ejecutar la aplicación interactiva (RECOMENDADO)
# ============================================================================
"""
Abrir terminal en: c:\Estudio\Deving\Proyecto\V2\app\
Ejecutar:
    python app.py

Luego:
    1. Registrar Usuario
       - Username: testuser
       - Password: 123456
    
    2. Login
       - Username: testuser
       - Password: 123456
    
    3. Explorar menú de usuario
"""


# ============================================================================
# OPCIÓN 2: Pruebas programáticas
# ============================================================================
"""
from database import DatabaseManager
from user_manager import UserManager
from resource_manager import ResourceManager
from reservation_manager import ReservationManager

# Inicializar
db = DatabaseManager()
user_mgr = UserManager(db)
resource_mgr = ResourceManager(db)
reservation_mgr = ReservationManager(db, resource_mgr)

# Test 1: Registrar usuario
print("Test 1: Registrando usuario...")
user_mgr.register_user("testuser", "password123")

# Test 2: Login
print("\nTest 2: Login...")
result = user_mgr.login("testuser", "password123")
print(f"Login result: {result}")

# Test 3: Ver usuarios
print("\nTest 3: Usuarios registrados:")
usuarios = user_mgr.get_all_users()
for user in usuarios:
    print(f"  - {user['username']} ({user['role']})")

# Test 4: Ver recursos
print("\nTest 4: Recursos:")
resource_mgr.show_resources_summary()

# Test 5: Ver reservas
print("\nTest 5: Reservas de testuser:")
vehicle, hotel = reservation_mgr.get_user_reservations("testuser")
print(f"  Vehículos: {len(vehicle)}")
print(f"  Hoteles: {len(hotel)}")
"""


# ============================================================================
# OPCIÓN 3: Importar clases individuales
# ============================================================================
"""
# Solo si necesitas una funcionalidad específica:

from database import DatabaseManager
db = DatabaseManager()

# Cargar datos
usuarios = db.load("login.json", [])
recursos = db.load_json_file("res_data")
reservas = db.load_json_file("reservations.json")

# Guardar datos
db.save("login.json", usuarios)
db.save_json_file("res_data", recursos)
"""


# ============================================================================
# ESTRUCTURA DE ARCHIVOS ACTUAL
# ============================================================================
"""
c:\Estudio\Deving\Proyecto\V2\
├── app/
│   ├── __main__.py              ← Ejecutable alternativo
│   ├── app.py                   ← ARCHIVO PRINCIPAL (python app.py)
│   ├── database.py              ← DatabaseManager
│   ├── user_manager.py          ← UserManager
│   ├── resource_manager.py      ← ResourceManager
│   ├── reservation_manager.py   ← ReservationManager
│   ├── menu_manager.py          ← MenuManager
│   ├── login.json               ← Datos de usuarios
│   ├── res_data                 ← Datos de recursos
│   └── reservations.json        ← Datos de reservas
│
├── README/
│   ├── QUICK_START.py           ← Este archivo
│   ├── ARQUITECTURA_OOP.py      ← Documentación de arquitectura
│   └── [otros documentos]
"""


# ============================================================================
# PRIMEROS PASOS
# ============================================================================
"""
1. Ejecutar:
   python c:\Estudio\Deving\Proyecto\V2\app\app.py

2. Registrar usuario (opción 1 en menú principal)
   Username: admin
   Password: admin123

3. Login (opción 2)
   Username: admin
   Password: admin123

4. Ver opciones de menú (si es admin: opciones de gestión)
   Si es user: opciones de reservas

5. Agregar recursos (si es admin):
   - Manage Resources → Add Hotel/Car/Driver
   
6. Hacer una reserva (si es user):
   - Rent Vehicle / Reserve Hotel
   
7. Ver y cancelar reservas:
   - View My Reservations
   - Cancel Reservation (mostrar ID de la reservación)
"""


# ============================================================================
# TROUBLESHOOTING
# ============================================================================
"""
Error: "ModuleNotFoundError: No module named 'database'"
   Solución: Ejecutar desde dentro de la carpeta app: c:\Estudio\Deving\Proyecto\V2\app\

Error: "File not found: login.json"
   Solución: Normal. Se crearán automáticamente al registrar usuarios

Error de import en otros módulos
   Solución: Verificar que todos los archivos .py estén en la carpeta app
"""


# ============================================================================
# INFORMACIÓN DE CONTACTO / SOPORTE
# ============================================================================
"""
Si necesitas:

✓ Modificar la interfaz CLI
   └─ Editar c:\Estudio\Deving\Proyecto\V2\app\menu_manager.py

✓ Agregar nuevos tipos de recursos
   └─ Extender c:\Estudio\Deving\Proyecto\V2\app\resource_manager.py

✓ Cambiar cómo se guardan datos
   └─ Modificar c:\Estudio\Deving\Proyecto\V2\app\database.py (ej: agregar SQL)

✓ Agregar nuevas validaciones
   └─ Extender user_manager.py o reservation_manager.py

✓ Agregar API REST
   └─ Crear api_manager.py que use las clases existentes

Cada componente es independiente y reutilizable.
"""
