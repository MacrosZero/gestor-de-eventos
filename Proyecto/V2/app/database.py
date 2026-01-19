"""
Database Manager - Maneja todas las operaciones con archivos JSON
"""
import json
import os
from typing import Any, Dict, List, Union


class DatabaseManager:
    """Gestiona la lectura y escritura de archivos JSON"""
    
    def __init__(self, base_dir: str = None):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            base_dir: Directorio base donde se almacenan los archivos JSON
        """
        self.base_dir = base_dir or os.path.dirname(__file__)
    
    def resolve_path(self, json_file: str) -> str:
        """Retorna el path absoluto de un archivo JSON"""
        return os.path.join(self.base_dir, json_file)
    
    def load(self, json_file: str, default: Any = None) -> Any:
        """
        Carga datos desde un archivo JSON.
        
        Args:
            json_file: Nombre del archivo JSON
            default: Valor por defecto si el archivo no existe o está vacío
            
        Returns:
            Datos del archivo o el valor por defecto
        """
        return self.load_json_file(json_file) or default
    
    def save(self, json_file: str, data: Any) -> bool:
        """
        Guarda datos en un archivo JSON de forma agnóstica.
        
        Args:
            json_file: Nombre del archivo JSON
            data: Datos a guardar (dict o list) - sin procesamiento especial
            
        Returns:
            True si se guardó exitosamente, False en caso contrario
        """
        return self.save_json_file(json_file, data)
    
    def load_json_file(self, json_file: str) -> Union[Dict, List]:
        """Carga un archivo JSON sin procesamiento especial"""
        path = self.resolve_path(json_file)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def save_json_file(self, json_file: str, data: Union[Dict, List]) -> bool:
        """Guarda un archivo JSON sin procesamiento especial"""
        path = self.resolve_path(json_file)
        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving to {json_file}: {e}")
            return False
