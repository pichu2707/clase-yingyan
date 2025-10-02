import os 
from pathlib import Path

"""
Configuración para el organizador de archivos MCP
Define las reglas de organizacíon por tipo de archivo
"""

#Ruta de carpetas de descargas (Windows)
DOWNLOADS_FOLDER = Path.home() / "Downloads"


# Diccionario de organización por extensiones
FILE_ORGANIZATION = {
    "Documentos": {
        "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
        "description": "Archivos de documentos y textos"
    },
    "Imágenes" : {
        "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "description": "Archivos de imágenes"
    },
    "Videos": {
        "extensions": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
        "description": "Archivos de video"
    },
    "Audio": {
        "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
        "description": "Archivos de audio"
    },
    "Programación": {
        "extensions": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".sql"],
        "description": "Archivos de código fuente"
    },
    "Comprimidos": {
        "extensions": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "description": "Archivos comprimidos"
    },
    "Ejecutables": {
        "extensions": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
        "description": "Archivos ejecutables e instaladores"
    },
    "Hojas de cálculo": {
        "extensions": [".xlsx", ".xls", ".csv", ".ods"],
        "description": "Archivos de hojas de cálculo"
    }
}


# Configuración adicionales
SETTINGS = {
    "create_date_folders": True, # Creamos subcarpetas por fechas
    "backup_before_move": False, # Crear copia de seguridad antes
    "dry_run": False, # Modo simulación (No mueve los archivos realmente )
    "log_operations": True, # Registrar las operaciones
}

def get_file_category(file_extension: str)-> str:
    """
    Determina la categoría de un archivo basado en su extensión

    Args:
        file_extension (str): Extension del archivo, por ejemplo, pdf

    Returns:
        str: Nombre de la cateogír o 'Otros' si no coincide
    """
    file_extension = file_extension.lower()

    for category, config in FILE_ORGANIZATION.items():
        if file_extension in config["extensions"]:
            return category
    return "Otros"

def get_target_folder(file_path:str, base_folder:str =None)-> str:
    """
        Calcula la carpeta ed desitno para un archivo

    Args: 
        file_path (Path): Ruta del archivo
        base_folder (Path): Carpeta base (Por defecto Descargas)
    
    Returns:
        Path: Ruta de la carpeta de destino
    """

    if base_folder is None:
        base_folder = DOWNLOADS_FOLDER

    #Obtener categoría del archivo
    category = get_file_category(file_path.suffix)

    #Carpeta de categoría
    target_folder = base_folder/"organizados"/category

    #Si está habilitado, crear subcarpeta por fecha
    if SETTINGS["create_date_folders"]:
        import datetime
        today = datetime.date.today()
        date_folder = f"{today.year}-{today.month:02d}"
        target_folder = target_folder/date_folder
    return target_folder