"""
Database Manager - Maneja todas las operaciones con archivos JSON
"""
import json
import os
from typing import Any, Dict, List, Union


class DatabaseManager:
    """Gestiona la lectura y escritura de archivos JSON"""
    
    def __init__(self, base_dir: str = None):
        """Inicializa el gestor de base de datos.

        Args:
            base_dir: Directorio base donde se almacenan los archivos JSON.
                Si es None, se usa el directorio del módulo (`__file__`).

        Notas:
            - Todas las operaciones de lectura/escritura usan rutas absolutas
              resueltas con `resolve_path`.
            - No se realizan cambios en disco hasta que se invoca `save_json_file`.
        """
        self.base_dir = base_dir or os.path.dirname(__file__)
    
    def resolve_path(self, json_file: str) -> str:
        """Construye y retorna el path absoluto para el archivo JSON dado.

        Args:
            json_file: Nombre de archivo relativo (por ejemplo 'res_data.json').

        Returns:
            Ruta absoluta que será utilizada para abrir/crear el archivo.
        """
        return os.path.join(self.base_dir, json_file)
    
    def load(self, json_file: str, default: Any = None) -> Any:
        """Carga datos desde `json_file` y devuelve `default` si el resultado es vacío.

        Args:
            json_file: Nombre del archivo JSON a leer.
            default: Valor que se retorna si el archivo no existe o está vacío.

        Returns:
            Contenido decodificado del JSON o `default` si no hay datos.
        """
        return self.load_json_file(json_file) or default
    
    def save(self, json_file: str, data: Any) -> bool:
        """Guarda `data` en `json_file` usando `save_json_file`.

        Args:
            json_file: Nombre del archivo JSON de destino.
            data: Estructura a serializar (dict o list).

        Returns:
            True si el guardado fue exitoso, False si ocurrió un error de IO.
        """
        return self.save_json_file(json_file, data)
    
    def load_json_file(self, json_file: str) -> Union[Dict, List]:
        """Lee y decodifica el archivo JSON indicado.

        Comportamiento:
            - Si el archivo no existe devuelve `{}`.
            - Si el JSON es inválido devuelve `{}`.

        Returns:
            Dict o List según el contenido del JSON; `{}` en caso de error o ausencia.
        """
        path = self.resolve_path(json_file)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def save_json_file(self, json_file: str, data: Union[Dict, List]) -> bool:
        """Serializa y guarda `data` en `json_file`.

        Args:
            json_file: Nombre del archivo de destino.
            data: Dict o List que será serializado a JSON.

        Returns:
            True si se guardó correctamente, False y se imprime el error en pantalla en caso contrario.
        """
        path = self.resolve_path(json_file)
        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving to {json_file}: {e}")
            return False
