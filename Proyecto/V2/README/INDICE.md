# ÍNDICE GENERAL DE DOCUMENTACIÓN - V2

Bienvenido a la documentación completa del Sistema de Gestión de Reservas V2.
Este índice centraliza TODA la información que necesitas según tu rol y necesidad.

**VERSIÓN:** 2.0 (OOP con Dependency Injection)  
**ESTADO:** Producción  
**ÚLTIMA ACTUALIZACIÓN:** Febrero 2026

---

## DOCUMENTOS DE REFERENCIA

📂 **Ubicación:** Proyecto/V2/README/

### 1. QUICK_START.md (⭐ COMIENZA AQUÍ)

**Propósito:** Ejecutar y probar la aplicación rápidamente

**Para quién:**
- Usuarios finales
- Desarrolladores jr
- Cualquiera que quiere empezar ahora

**Contiene:**
- 3 opciones para ejecutar (interactive, programmatic, import)
- Instrucciones paso a paso
- Estructura de archivos
- Primeros pasos de usuario
- Solución de problemas comunes
- Atajos rápidos
- Arquitectura simplificada
- Próximos pasos

**Lectura típica:** 15-20 minutos  
**Necesidad principal:** "¿Cómo ejecuto esto?"

---

### 2. ARQUITECTURA_OOP.md (📐 COMPRENSIÓN TÉCNICA)

**Propósito:** Entender cómo está construido el sistema internamente

**Para quién:**
- Desarrolladores
- Arquitectos
- Cualquiera que quiere extender
- Code reviewers

**Contiene:**
- Visión general de arquitectura
- Diagrama de dependencias
- 6 clases principales (detalladas)
- Métodos públicos/privados
- Responsabilidades
- Patrones de diseño (SOLID, DI, Strategy)
- Inyección de dependencias
- Flujo de datos y control
- Extensibilidad futura
- Casos de uso (API REST, SQL, etc.)
- Ejemplos de código
- Beneficios arquitectónicos

**Lectura típica:** 45-60 minutos  
**Necesidad principal:** "¿Cómo funciona internamente?"

---

### 3. CHANGELOG_V1_V2.md (🔄 MIGRACIÓN DE VERSIONES)

**Propósito:** Entender qué cambió de V1 a V2 y por qué

**Para quién:**
- Desarrolladores que conocen V1
- Equipo de desarrollo
- Personas que quieren entender decisiones
- Estudiantes de arquitectura de software

**Contiene:**
- Resumen ejecutivo de cambios
- Comparativa estructural (V1 vs V2)
- Mapeo detallado de migración
- Cambios en persistencia de datos
- Cambios en seguridad (passwords)
- Cambios en gestión de IDs de reservas
- Cambios en validación (exclusión mutua)
- Cambios en cada módulo
- Estadísticas de cambio
- Beneficios de la migración
- Conclusión y lecciones

**Lectura típica:** 45-60 minutos  
**Necesidad principal:** "¿Qué cambió y por qué?"

---

### 4. INDICE.md (este archivo)

**Propósito:** Navegar todos los documentos según tu necesidad

**Para quién:** Todos (punto de partida)

**Contiene:**
- Guía de este mismo índice
- Mapas de lectura por rol/necesidad
- Estructura del proyecto
- Conceptos clave con referencias
- Preguntas frecuentes con respuestas
- Comandos rápidos
- Timeline de lectura
- Estado actual

---

## MAPA DE LECTURA SEGÚN TU NECESIDAD

❓ **"Necesito ejecutar la app AHORA"**
- Tiempo: 5 minutos
- Lee: [QUICK_START.md](QUICK_START.md) → "OPCIÓN 1"
- Resultado: Aplicación corriendo

❓ **"Quiero entender cómo funciona"**
- Tiempo: 60 minutos
- Lee: [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → Completo
- Luego: Abre app.py en editor
- Resultado: Comprensión de arquitectura

❓ **"Vengo de V1, ¿qué cambió?"**
- Tiempo: 60 minutos
- Lee: [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md) → "Resumen Ejecutivo"
- Luego: [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md) → Completo
- Finalmente: [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Patrones de Diseño"
- Resultado: Comprensión de migración

❓ **"¿Cómo registro un usuario?"**
- Tiempo: 10 minutos
- Lee: [QUICK_START.md](QUICK_START.md) → "Primeros Pasos"
- Resultado: Usuario creado

❓ **"¿Cómo hago una reserva?"**
- Tiempo: 10 minutos
- Lee: [QUICK_START.md](QUICK_START.md) → "Flujo Típico de Usuario"
- Resultado: Reserva creada

❓ **"¿Cómo agrego una nueva feature?"**
- Tiempo: 90 minutos
- Lee: [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Patrones Avanzados"
- Lee: [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md) → "Cómo Contribuir"
- Abre: resource_manager.py o user_manager.py
- Resultado: Feature agregada correctamente

❓ **"¿Cómo cambio a SQL?"**
- Tiempo: 120 minutos
- Lee: [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Patrones Avanzados"
- Lee: database.py (comprende interfaz)
- Crea: SQLDatabaseManager
- Resultado: Migración a SQL completa

❓ **"¿Cómo creo un API REST?"**
- Tiempo: 180 minutos
- Lee: [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Extensibilidad Futura" (API REST)
- Instala: Flask o FastAPI
- Crea: api_routes.py
- Resultado: API funcional

❓ **"Tengo un error, ¿qué hago?"**
- Tiempo: 5-15 minutos
- Lee: [QUICK_START.md](QUICK_START.md) → "Solución de Problemas"
- Resultado: Error resuelto

---

## GUÍA POR ROL/PERFIL

### 👤 USUARIO FINAL (Solo quiero usar la app)

**Documentación mínima:**
- [QUICK_START.md](QUICK_START.md) → "OPCIÓN 1" (ejecutar)
- [QUICK_START.md](QUICK_START.md) → "Flujo Típico de Usuario"
- [QUICK_START.md](QUICK_START.md) → "Solución de Problemas"
- Total: 20 minutos

**Punto de partida:** [QUICK_START.md](QUICK_START.md)

---

### 👨‍💻 DESARROLLADOR JUNIOR

**Documentación recomendada:**
- [QUICK_START.md](QUICK_START.md) → Completo (entender cómo usar)
- [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Visión General" (contexto)
- [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Descripción de Clases" (qué hace qué)
- app.py (código realmente corto, leerlo)
- user_manager.py (ejemplo de Manager)
- Total: 120 minutos

**Punto de partida:** [QUICK_START.md](QUICK_START.md)

---

### 👨‍💼 DESARROLLADOR SENIOR

**Documentación recomendada:**
- [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md) → "Cambios en Arquitectura"
- [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → Completo
- Todo el código (app.py, managers, database.py)
- Revisar patrones SOLID
- Total: 180 minutos

**Punto de partida:** [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md)

---

### 🏗️ ARQUITECTO / LÍDER TÉCNICO

**Documentación recomendada:**
- [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md) → "Beneficios de la Migración"
- [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Patrones de Diseño"
- [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Extensibilidad Futura"
- Planificar: tests, logging, deployment
- Total: 120 minutos

**Punto de partida:** [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md)

---

### 🔧 DEVOPS / DEPLOYMENT

**Documentación recomendada:**
- [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Extensibilidad Futura"
- database.py (comprende cómo usar)
- Nota: DatabaseManager es agnóstico (SQL ready)
- Planificar: Docker, CI/CD
- Total: 60 minutos

**Punto de partida:** [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md)

---

### 📚 ESTUDIANTE / PRINCIPIANTE EN OOP

**Documentación recomendada:**
- [QUICK_START.md](QUICK_START.md) → "Ejecutar" (experiencia)
- [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md) → "V1 vs V2" (comparación)
- [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → "Patrones de Diseño"
- [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md) → Ejemplo de Strategy
- Total: 150 minutos

**Punto de partida:** [QUICK_START.md](QUICK_START.md)

---

## ESTRUCTURA DEL PROYECTO

```
Proyecto/V2/
│
├── app/                          ← CÓDIGO FUENTE
│   ├── __main__.py              Ejecutor alternativo
│   ├── app.py                   ReservationApp (orquestadora)
│   ├── database.py              DatabaseManager (persistencia)
│   ├── user_manager.py          UserManager (usuarios + auth)
│   ├── resource_manager.py      ResourceManager (recursos)
│   ├── reservation_manager.py   ReservationManager (reservas)
│   ├── menu_manager.py          MenuManager (interfaz CLI)
│   │
│   ├── login.json               {"users": [...]}
│   ├── res_data.json            {"hotels": [...], "cars": [...], "chofer": [...]}
│   └── reservations.json        {"vehicle_reservations": [...], "hotel_reservations": [...]}
│
└── README/                       ← DOCUMENTACIÓN (esta carpeta)
    ├── INDICE.md               ← Estás aquí
    ├── QUICK_START.md          Para empezar
    ├── ARQUITECTURA_OOP.md     Entender internals
    └── CHANGELOG_V1_V2.md      Ver qué cambió

Ver estructura completa de V1:
└── ../V1/
    ├── login.py                (V1 procedural)
    ├── res_mgmt.py
    ├── event_gestor.py
    ├── menus.py
    └── [datos JSON]
```

---

## CONCEPTOS CLAVE CON REFERENCIAS

### INYECCIÓN DE DEPENDENCIAS (Dependency Injection - DI)

**¿Qué es?**
- En lugar de que clase A cree clase B, B se "inyecta" en A

**Ejemplo en código:**
```python
# SIN DI (acoplado):
class UserManager:
    def __init__(self):
        self.db = DatabaseManager()  # ← Acoplado

# CON DI (desacoplado):
class UserManager:
    def __init__(self, db: DatabaseManager):
        self.db = db  # ← Inyectado

# En app.py:
db = DatabaseManager()
user_mgr = UserManager(db)  # ← Se inyecta
```

**¿Por qué?**
- Bajo acoplamiento
- Fácil testear (mockear db)
- Fácil cambiar implementación
- Más flexible

**Referencia completa:** [ARQUITECTURA_OOP.md → Patrones de Diseño](ARQUITECTURA_OOP.md#patrones-de-diseño-aplicados)

---

### SINGLE RESPONSIBILITY PRINCIPLE (SRP)

**¿Qué es?**
- Cada clase debe tener UNA única responsabilidad

**Ejemplo en V2:**
- DatabaseManager → Solo persistencia (JSON)
- UserManager → Solo usuarios y autenticación
- ResourceManager → Solo recursos
- ReservationManager → Solo reservas
- MenuManager → Solo interfaz
- ReservationApp → Solo orquestación

**¿Por qué?**
- Código más limpio
- Fácil entender cada clase
- Fácil testear
- Cambios no se propagan

**Referencia completa:** [CHANGELOG_V1_V2.md → Beneficios de la Migración](CHANGELOG_V1_V2.md#beneficios-de-la-migración)

---

### PATRÓN STRATEGY

**¿Qué es?**
- Intercambiar implementación sin cambiar interfaz

**Ejemplo: Cambiar a SQL**
```python
class SQLDatabaseManager(DatabaseManager):
    def load_json_file(self, filename):
        # Implementación SQL
        pass

# En app.py: Un cambio
self.db = SQLDatabaseManager()
# Todos los Managers funcionan igual
```

**Referencia completa:** [ARQUITECTURA_OOP.md → Patrones de Diseño](ARQUITECTURA_OOP.md#patrones-de-diseño-aplicados)

---

### EXCLUSIÓN MUTUA

**¿Qué es?**
- Solo un recurso puede estar reservado en un rango de fechas

**Fórmula de solapamiento:**
```python
if (start_req < res_end) and (res_start < end_req):
    ocupada = True
```

**Ejemplo:**
```
Reserva A: 2026-02-05 a 2026-02-10
Reserva B: 2026-02-08 a 2026-02-12

¿Se solapan? 
start_req(8) < res_end(10) and res_start(5) < end_req(12)
True and True = True (SÍ, se solapan)
```

**Referencia completa:** [CHANGELOG_V1_V2.md → Cambios en Gestión de Reservas](CHANGELOG_V1_V2.md#cambios-en-gestión-de-reservas-ids)

---

### IDs ÚNICOS

**¿Qué es en V2?**
- Timestamp ISO: 2026-02-04T14:30:45.123456

**¿Por qué?**
- Único globalmente
- Auditable (cuándo se creó)
- Estándar (como MongoDB)
- Robusto (no cambia si otros datos cambian)

**Referencia completa:** [CHANGELOG_V1_V2.md → Cambios en Gestión de IDs](CHANGELOG_V1_V2.md#cambios-en-gestión-de-reservas-ids)

---

### AGNÓSTICO

**¿Qué significa?**
- DatabaseManager no sabe de usuarios, reservas, etc.

**Beneficio:**
- Cambiar de JSON a SQL solo requiere cambiar DatabaseManager

**Referencia completa:** [CHANGELOG_V1_V2.md → Cambios en Persistencia](CHANGELOG_V1_V2.md#cambios-clave-en-persistencia)

---

## PREGUNTAS FRECUENTES

**P: ¿Dónde está el punto de entrada de la aplicación?**
- R: app.py
  - if __name__ == "__main__": main()
  - O: python -m __main__

**P: ¿Cuántas clases principales hay?**
- R: 7 (1 orquestadora + 6 managers)
  - ReservationApp (app.py)
  - DatabaseManager (database.py)
  - UserManager (user_manager.py)
  - ResourceManager (resource_manager.py)
  - ReservationManager (reservation_manager.py)
  - MenuManager (menu_manager.py)

**P: ¿Cuál es la diferencia V1 vs V2?**
- R: V1 = procedural, V2 = OOP
  - Lee: [CHANGELOG_V1_V2.md → Resumen Ejecutivo](CHANGELOG_V1_V2.md#resumen-ejecutivo)

**P: ¿Cómo evito double-booking?**
- R: Exclusión mutua (ya implementada)
  - Fórmula: if (start_req < res_end) and (res_start < end_req)
  - Ver: [ARQUITECTURA_OOP.md → ReservationManager](ARQUITECTURA_OOP.md#5-reservationmanager-reservation_managerpy---gestión-de-reservas)

**P: ¿Dónde está la lógica de login?**
- R: user_manager.py → UserManager.login()
  - Usa hash SHA256+PBKDF2

**P: ¿Cómo está estructurada la BD?**
- R: 3 archivos JSON
  - login.json → {"users": [...]}
  - res_data.json → {"hotels": [...], "cars": [...], "chofer": [...]}
  - reservations.json → {"vehicle_reservations": [...], ...}

**P: ¿Puedo cambiar a SQL?**
- R: Sí, solo necesitas:
  - Crear SQLDatabaseManager (extiende DatabaseManager)
  - Implementar load_json_file() y save_json_file()
  - Cambiar un línea en ReservationApp
  - ¡Todo lo demás funciona igual!

**P: ¿Cómo agrego una nueva feature?**
- R: Seguir SOLID + inyectar dependencias
  - Ver: [CHANGELOG_V1_V2.md → Cómo Contribuir](CHANGELOG_V1_V2.md#conclusión)

**P: ¿Qué es "Inyección de Dependencias"?**
- R: En lugar de que clase A cree B, B se inyecta en A
  - Ver: [ARQUITECTURA_OOP.md → Patrones de Diseño](ARQUITECTURA_OOP.md#patrones-de-diseño-aplicados)

**P: ¿Los passwords están seguros?**
- R: Sí, SHA256 + PBKDF2 (100k iteraciones)
  - Ver: [CHANGELOG_V1_V2.md → Cambios en Seguridad](CHANGELOG_V1_V2.md#cambios-en-seguridad-passwords)

**P: ¿Cómo sé el ID de mi reserva?**
- R: Usa "Ver mis reservas" en la app
  - ID es un timestamp ISO

**P: ¿Qué significa "agnóstico"?**
- R: DatabaseManager no sabe nada de usuarios, reservas, etc.
  - Cada Manager prepara su propio formato
  - Fácil cambiar implementación

**P: ¿Hay tests unitarios?**
- R: No (planeado para V2.1)
  - Estructura OOP lo permite fácilmente

---

## COMANDOS RÁPIDOS

**Ejecutar aplicación:**
```bash
cd Proyecto/V2/app
python app.py
```

**Ejecutar como módulo:**
```bash
cd Proyecto/V2/app
python -m __main__
```

**Ver estructura:**
```bash
# Windows
dir /s Proyecto/V2/app

# Linux
ls -R Proyecto/V2/app
```

**Editar documentación:**
- Abre en editor: README/QUICK_START.md
- Abre en editor: README/ARQUITECTURA_OOP.md
- Abre en editor: README/CHANGELOG_V1_V2.md

**Ver archivos de datos:**
- Abre: app/login.json
- Abre: app/res_data.json
- Abre: app/reservations.json

**Revisar estructura de código:**
- Abre: app/app.py (pequeño, lee primero)
- Abre: app/database.py
- Abre: app/user_manager.py (ejemplo de Manager)

---

## ESTADO ACTUAL DEL PROYECTO

**✅ COMPLETADO EN V2**
- Arquitectura OOP con 6 Managers
- Inyección de Dependencias
- SOLID Principles (SRP, DIP, etc.)
- Exclusión mutua de reservas
- IDs únicos (timestamps)
- Hashing de passwords (SHA256+PBKDF2)
- Desacoplamiento total
- DatabaseManager agnóstico
- Documentación 100%
- Código limpio y legible
- Listo para producción (con tests)

**🟡 PLANEADO PARA V2.1**
- Tests unitarios (pytest)
- Encriptación adicional
- Logging centralizado
- Migración a SQL (ejemplo)
- API REST (Flask)
- CI/CD (GitHub Actions)

**🔴 FUTURO (V3)**
- Autenticación JWT
- Frontend web (React)
- Docker + Kubernetes
- Caché (Redis)
- Notificaciones en tiempo real

**❌ NO INICIADO**
- [Espera tu contribución]

---

## CONCLUSIÓN

Tienes TODO lo que necesitas para:

- ✓ Ejecutar la aplicación
- ✓ Entender la arquitectura
- ✓ Extender funcionalidades
- ✓ Contribuir código
- ✓ Cambiar a SQL
- ✓ Crear API REST
- ✓ Depurar problemas
- ✓ Entrenar otros

¡Bienvenido a V2!

**Punto de partida recomendado:**
- Si ejecutas primero: [QUICK_START.md](QUICK_START.md)
- Si estudias primero: [ARQUITECTURA_OOP.md](ARQUITECTURA_OOP.md)
- Si migras de V1: [CHANGELOG_V1_V2.md](CHANGELOG_V1_V2.md)

¿Preguntas?
- Ver "Preguntas Frecuentes" en este documento
- O buscar en el documento relevante

¡Happy coding!
