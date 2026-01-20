# Gestor de Eventos (Deving)

Repositorio que contiene todo el contenido de la carpeta `Deving` (proyectos, scripts y utilidades).

Estructura principal:

- Testing.py
- Proyecto/
  - V1/
  - V2/

Instrucciones rápidas:

1. Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # si agregas requerimientos
```

2. Ejecutar la aplicación (ejemplo para V2/app):

```powershell
$env:PYTHONPATH="C:\Estudio\Deving\Proyecto\V2\app"
python C:\Estudio\Deving\Proyecto\V2\app\__main__.py
```

3. Tests:

```powershell
$env:PYTHONPATH="C:\Estudio\Deving\Proyecto\V2\app"
python -m unittest discover -v Proyecto\V2\app\tests
```
