# QUICK START - Guía rápida para probar el sistema

Bienvenido al Sistema de Gestión de Reservas V2.
Esta guía te ayudará a ejecutar y probar la aplicación en minutos.

---

## OPCIÓN 1: Ejecutar la aplicación interactiva (RECOMENDADO) ⭐

### PASOS:

1. Abre una terminal/PowerShell en: `Proyecto/V2/app/`

2. Ejecuta uno de estos comandos:
   ```bash
   python app.py
   ```
   
   O alternativamente:
   ```bash
   python -m __main__
   ```

3. Sigue el menú interactivo:
   
   **Primera vez:**
   - Selecciona "1. Register User"
      - Username: testuser
      - Password: 123456
   
   **Luego:**
   - Selecciona "2. Login"
      - Username: testuser
      - Password: 123456
   
   **Como usuario normal podrás:**
   - Ver tu perfil
   - Rentar vehículos
   - Reservar hoteles
   - Ver y cancelar reservas
   
   **Como administrador podrás:**
   - Ver todos los usuarios
   - Promover usuarios a admin
   - Gestionar recursos (hoteles, autos, choferes)
   - Ver datos de recursos

**Presiona Ctrl+C para salir en cualquier momento**

---

## OPCIÓN 2: Pruebas programáticas en Python

Para hacer pruebas rápidas sin interfaz interactiva, crea un archivo `test.py`:

```python
from app import ReservationApp

# Inicializar aplicación
app = ReservationApp()

# Acceder a los managers
db = app.db
user_mgr = app.user_mgr
resource_mgr = app.resource_mgr
reservation_mgr = app.reservation_mgr

# Test 1: Registrar usuario
print("Test 1: Registrando usuario...")
user_mgr.register_user("testuser2", "password456")

# Test 2: Login
print("\nTest 2: Login...")
result = user_mgr.login("testuser2", "password456")
if result:
    username, password_hash, role = result
    print(f"Login exitoso: {username} ({role})")

# Test 3: Ver todos los usuarios
print("\nTest 3: Usuarios registrados:")
usuarios = user_mgr.get_all_users()
for user in usuarios:
    print(f"  - {user['username']} ({user['role']})")

# Test 4: Ver recursos
print("\nTest 4: Resumen de Recursos:")
resource_mgr.show_resources_summary()

# Test 5: Ver reservas de un usuario
print("\nTest 5: Reservas de testuser2:")
reservations = reservation_mgr.get_user_reservations("testuser2")
if isinstance(reservations, dict):
    vehicle_res = reservations.get('vehicle_reservations', [])
    hotel_res = reservations.get('hotel_reservations', [])
    print(f"  Vehículos: {len(vehicle_res)}")
    print(f"  Hoteles: {len(hotel_res)}")
```

---

## OPCIÓN 3: Importar clases individuales

Para usar componentes específicos en tu propio código:

### Opción A: Crear la app y acceder a componentes

```python
from app import ReservationApp

app = ReservationApp(base_dir="./app")
db = app.db
user_mgr = app.user_mgr
resource_mgr = app.resource_mgr
```

### Opción B: Importar directamente (si tienes los módulos en PYTHONPATH)

```python
from database import DatabaseManager
from user_manager import UserManager
from resource_manager import ResourceManager

db = DatabaseManager(base_dir="./app")
user_mgr = UserManager(db)
resource_mgr = ResourceManager(db)

# Cargar datos
usuarios = user_mgr.get_all_users()
recursos = resource_mgr.load_resources()

# Guardar datos
user_mgr.register_user("new_user", "password123")
```

---

## ESTRUCTURA DE ARCHIVOS ACTUAL

```
Proyecto/V2/
├── app/
│   ├── __main__.py                  ← Punto de entrada alternativo (python -m app)
│   ├── app.py                       ← ReservationApp - Orquestador principal
│   ├── database.py                  ← DatabaseManager - Gestión de persistencia
│   ├── user_manager.py              ← UserManager - Autenticación y usuarios
│   ├── resource_manager.py          ← ResourceManager - Hoteles, autos, choferes
│   ├── reservation_manager.py       ← ReservationManager - Reservas y disponibilidad
│   ├── menu_manager.py              ← MenuManager - Interfaz interactiva CLI
│   │
│   ├── login.json                   ← Base de datos: {"users": [...]}
│   ├── res_data.json                ← Base de datos: {"hotels": [...], "cars": [...], "chofer": [...]}
│   └── reservations.json            ← Base de datos: {"vehicle_reservations": [...], "hotel_reservations": [...]}
│
└── README/
    ├── QUICK_START.md               ← Tú estás aquí (ejecución rápida)
    ├── ARQUITECTURA_OOP.md          ← Entender la arquitectura interna
    ├── CHANGELOG_V1_V2.md           ← Cambios de V1 a V2
    └── INDICE.md                    ← Índice completo de documentación
```

---

## FLUJO TÍPICO DE USUARIO

1. Ejecuta: `python app.py`
2. Verás el menú principal con opciones:
   - Register User
   - Login
   - Exit

3. Registra un usuario nuevo:
   - Username: myuser
   - Password: mypassword

4. Haz login con esas credenciales

5. Si eres usuario normal (role: user), podrás:
   - Ver tu perfil
   - Rentar vehículos (si existen recursos)
   - Reservar hoteles (si existen recursos)
   - Ver tus reservas
   - Cancelar reservas por ID

6. Si eres administrador (role: admin), podrás:
   - Ver todos los usuarios
   - Promover otros usuarios a admin
   - Gestionar recursos:
     * Agregar hoteles
     * Agregar vehículos
     * Agregar choferes
   - Ver resumen de recursos

7. Logout para salir de la sesión

---

## SOLUCIÓN DE PROBLEMAS COMUNES

**P: "ModuleNotFoundError: No module named 'database'"**
- R: Asegúrate de ejecutar el comando desde `Proyecto/V2/app/`
  ```bash
  cd Proyecto/V2/app
  python app.py
  ```

**P: "FileNotFoundError: login.json"**
- R: Los archivos JSON se crean automáticamente cuando los necesitan.
  Simplemente registra un usuario y se crearán.

**P: "¿Cómo me hago administrador?"**
- R: Opción 1: Edita login.json y cambia `"role": "user"` a `"role": "admin"`
  - Opción 2: Usa la opción de menú "Make Admin" si ya eres admin

**P: "¿Cómo limpio todos los datos?"**
- R: Elimina los archivos JSON:
   - Elimina login.json
   - Elimina res_data.json
   - Elimina reservations.json
   - Se recrearán al ejecutar la app.

**P: "¿Cómo sé el ID de mi reserva?"**
- R: Usa "View My Reservations" y verás todos tus reservas con su ID único.

**P: "¿Es seguro guardar passwords así?"**
- R: Se usa SHA256 con PBKDF2 (100,000 iteraciones). Adecuado para desarrollo.
  Para producción, considera usar Django Auth o bcrypt.

---

## ATAJOS RÁPIDOS

✓ **Crear usuario admin rápidamente:**
  1. Registra: admin / admin123
  2. Haz login
  3. Edita login.json y cambia `"role": "admin"` en el usuario admin
  4. Vuelve a hacer login

✓ **Probar funcionalidad de recursos:**
  1. Haz admin
  2. Usa "Manage Resources" para agregar:
     - Hotel: "Paradise Hotel", "Miami", 50 rooms, $100/night
     - Car: "Toyota Camry", 5 units available
     - Driver: "John Doe", "Commercial License"
  3. Cambia a usuario normal
  4. Intenta rentar vehículo o reservar hotel

✓ **Ver datos en crudo:**
  - Abre login.json con cualquier editor de texto
  - Abre res_data.json con cualquier editor de texto
  - Abre reservations.json con cualquier editor de texto
  
✓ **Hacer tests rápidos desde Python:**
  ```python
  python
  >>> from app import ReservationApp
  >>> app = ReservationApp()
  >>> app.user_mgr.get_all_users()
  >>> app.resource_mgr.load_resources()
  ```

---

## ARQUITECTURA SIMPLIFICADA

```
                      ReservationApp
                     (Orquestadora)
                          │
                ┌─────────┼─────────┐
                │         │         │
          DatabaseMgr  MenuManager  │
                │         │         │
                └─────────┼─────────┘
                │         │         │
            UserMgr  ResrceMgr  ReservationMgr
                ▲                   ▲
                └───────────────────┘
                (Persistencia central)
```

Cada Manager es independiente y reutilizable.
DatabaseManager es agnóstico a la estructura de datos (fácil migrar a SQL/MongoDB).

---

## PRÓXIMOS PASOS

Después de probar la aplicación:

1. Lee [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) para entender cómo está construido
2. Lee [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md) para ver qué cambió de V1 a V2
3. Abre los archivos .py en el editor para ver el código
4. Modifica features según tus necesidades
5. Consulta [INDICE.md](INDICE.md) para más documentación

La aplicación está lista para extender con:
- API REST usando Flask/FastAPI
- Base de datos SQL
- Interfaz web
- Sistema de notificaciones
- etc.
