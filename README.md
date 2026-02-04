# Informe Técnico: Planificador Inteligente de Eventos Logísticos

## 1. Introducción

El sistema desarrollado consiste en un motor de planificación y gestión de recursos enfocado en el dominio de la **logística turística**. Esta elección se fundamentó en la posibilidad de obtener retroalimentación directa de profesionales del sector, permitiendo modelar escenarios reales de ocupación hotelera y transporte de pasajeros.

La aplicación permite la gestión de dos tipos de eventos principales: **estancias en complejos hoteleros** y **alquiler de flota vehicular**. Para garantizar la integridad operativa, se definieron e implementaron las siguientes restricciones de negocio:

* **Restricción Temporal:** No se permite la creación de reservas con una antelación inferior a 72 horas respecto a la fecha actual.
* **Restricción de Simultaneidad:** Se impide que un mismo usuario mantenga dos reservas activas del mismo tipo para el mismo periodo de tiempo.
* **Restricción de Competencia:** Para la contratación de choferes, el sistema valida estrictamente que la licencia del conductor (e.g., Tipo C) coincida con el requerimiento técnico del vehículo (e.g., Bus).
* **Restricción de Identidad:** Se exige la creación de cuentas únicas donde el nombre de usuario es un identificador irrepetible en la base de datos.

---

## 2. Estructura del Proyecto

Se implementó una arquitectura basada en el paradigma de **Programación Orientada a Objetos (OOP)**, dividiendo la aplicación en módulos especializados que interactúan entre sí:

* **`DatabaseManager`**: Funciona como la capa de acceso a datos (DAO), centralizando la lectura y escritura de archivos.
* **`UserManager`**: Gestiona el ciclo de vida de los usuarios, la autenticación y el control de acceso por roles.
* **`ResourceManager`**: Administra el inventario de activos (hoteles, coches y personal).
* **`ReservationManager`**: Actúa como el motor de reglas de negocio, donde se procesan las validaciones de fechas, disponibilidad de inventario ("Pools") y cálculo de costos.
* **`MenuManager`**: Despliega la interfaz de línea de comandos (CLI), desacoplando la interacción con el usuario de la lógica interna.

---

## 3. Fase de Diseño y Toma de Decisiones

Durante la fase de diseño, se decidió utilizar **JSON** como formato de persistencia de datos. Esta decisión se tomó basándose en las recomendaciones técnicas recibidas y en la facilidad que ofrece este formato para la inspección y depuración manual de los datos durante el desarrollo.

En cuanto a la metodología de desarrollo, se optó por una transición desde un modelo procedural hacia uno de clases. Para este proceso de refactorización, se emplearon herramientas de asistencia basada en inteligencia artificial (GitHub Copilot y Claude Haiku 4.5). La estructura generada fue sometida a un proceso de **revisión manual exhaustiva**, donde se corrigieron inconsistencias lógicas en el flujo de datos y se ajustaron los métodos para cumplir fielmente con los requisitos del dominio turístico.

---

## 4. Problemas Enfrentados y Soluciones

A lo largo de la implementación, se identificaron y resolvieron los siguientes retos técnicos:

* **Persistencia de Datos:** Se detectaron errores críticos cuando el sistema intentaba acceder a archivos JSON inexistentes. Para mitigar esto, se implementó una lógica de control de excepciones mediante bloques `try-except` y la creación automatizada de estructuras de datos iniciales en caso de ausencia de archivos.
* **Sincronización de Recursos:** La validación de la disponibilidad de choferes y vehículos requirió un manejo preciso de los estados de los objetos. Se resolvió mediante la comparación de intervalos temporales, asegurando que un recurso no fuera contabilizado como disponible si existía un solapamiento en el cronograma de reservas.
* **Refactorización de Código:** El mayor desafío consistió en limpiar el código generado por las herramientas de IA, las cuales inicialmente omitían validaciones de seguridad básicas que fueron añadidas posteriormente de forma manual para robustecer el sistema.

---

## 5. Lógica del Sistema (Back-end)

El núcleo del software no se limita a almacenar datos; ejecuta un proceso de validación en cascada. Por ejemplo, al solicitar un vehículo con chofer, el sistema primero verifica el stock físico del vehículo; posteriormente, consulta la tabla de personal para filtrar aquellos conductores que poseen la licencia adecuada y, finalmente, comprueba que ninguna reserva previa colisione con las fechas solicitadas.

Todas las operaciones de fecha se manejan mediante el módulo `datetime`, permitiendo que la restricción de las 72 horas se calcule de forma dinámica restando el tiempo de ejecución actual del tiempo de inicio del evento:
