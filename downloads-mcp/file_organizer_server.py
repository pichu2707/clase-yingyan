"""
Servidor MCP para organizar archivos de la carpeta de descargas
Implementa herramientas para analizar, organizar y gestionar archivos
Version sin emojis - compatible con cualquier codificacion
"""

import asyncio
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Importaciones MCP actualizadas
import mcp.types as types
from mcp.server import Server
from pydantic import AnyUrl

from config import (
    DOWNLOADS_FOLDER, 
    FILE_ORGANIZATION, 
    SETTINGS,
    get_file_category,
    get_target_folder
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("file-organizer-mcp")

# Crear servidor MCP
server = Server("file-organizer")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Retorna la lista de herramientas disponibles"""
    return [
        types.Tool(
            name="analyze_downloads",
            description="Analiza los archivos en la carpeta de descargas y muestra estadísticas",
            inputSchema={
                "type": "object",
                "properties": {
                    "show_details": {
                        "type": "boolean",
                        "description": "Mostrar detalles de cada archivo",
                        "default": False
                    }
                }
            }
        ),
        types.Tool(
            name="organize_files",
            description="Organiza los archivos de descargas en carpetas por categoría",
            inputSchema={
                "type": "object",
                "properties": {
                    "dry_run": {
                        "type": "boolean",
                        "description": "Simular la organización sin mover archivos",
                        "default": True
                    },
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Categorías específicas a organizar (opcional)"
                    }
                }
            }
        ),
        types.Tool(
            name="create_folder_structure",
            description="Crea la estructura de carpetas para organización",
            inputSchema={
                "type": "object",
                "properties": {
                    "base_folder": {
                        "type": "string",
                        "description": "Carpeta base donde crear la estructura"
                    }
                }
            }
        ),
        types.Tool(
            name="get_file_info",
            description="Obtiene información detallada de un archivo específico",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Nombre del archivo a analizar"
                    }
                },
                "required": ["filename"]
            }
        ),
        types.Tool(
            name="cleanup_empty_folders",
            description="Elimina carpetas vacías de la estructura organizada",
            inputSchema={
                "type": "object",
                "properties": {
                    "dry_run": {
                        "type": "boolean",
                        "description": "Simular la limpieza sin eliminar carpetas",
                        "default": True
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """Maneja las llamadas a las herramientas"""
    
    if name == "analyze_downloads":
        return await analyze_downloads(arguments.get("show_details", False))
    
    elif name == "organize_files":
        return await organize_files(
            arguments.get("dry_run", True),
            arguments.get("categories")
        )
    
    elif name == "create_folder_structure":
        return await create_folder_structure(
            arguments.get("base_folder", str(DOWNLOADS_FOLDER))
        )
    
    elif name == "get_file_info":
        return await get_file_info(arguments["filename"])
    
    elif name == "cleanup_empty_folders":
        return await cleanup_empty_folders(arguments.get("dry_run", True))
    
    else:
        raise ValueError(f"Herramienta desconocida: {name}")

async def analyze_downloads(show_details: bool) -> list[types.TextContent]:
    """Analiza los archivos en la carpeta de descargas"""
    try:
        if not DOWNLOADS_FOLDER.exists():
            return [types.TextContent(
                type="text",
                text=f"[ERROR] La carpeta de descargas no existe: {DOWNLOADS_FOLDER}"
            )]
        
        # Obtener todos los archivos
        files = [f for f in DOWNLOADS_FOLDER.iterdir() if f.is_file()]
        
        if not files:
            return [types.TextContent(
                type="text",
                text="[INFO] La carpeta de descargas está vacía"
            )]
        
        # Analizar por categorías
        categories = {}
        total_size = 0
        
        for file_path in files:
            category = get_file_category(file_path.suffix)
            if category not in categories:
                categories[category] = []
            
            file_size = file_path.stat().st_size
            file_info = {
                "name": file_path.name,
                "size": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2),
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime)
            }
            
            categories[category].append(file_info)
            total_size += file_size
        
        # Generar reporte
        report = f"[ANÁLISIS] Carpeta de descargas\n\n"
        report += f"Carpeta: {DOWNLOADS_FOLDER}\n"
        report += f"Total de archivos: {len(files)}\n"
        report += f"Tamaño total: {round(total_size / (1024 * 1024), 2)} MB\n\n"
        
        report += "Distribución por categorías:\n"
        for category, file_list in sorted(categories.items()):
            count = len(file_list)
            category_size = sum(f["size"] for f in file_list)
            category_size_mb = round(category_size / (1024 * 1024), 2)
            
            report += f"• {category}: {count} archivos ({category_size_mb} MB)\n"
            
            if show_details:
                for file_info in sorted(file_list, key=lambda x: x["size"], reverse=True)[:5]:
                    report += f"  - {file_info['name']} ({file_info['size_mb']} MB)\n"
                if len(file_list) > 5:
                    report += f"  ... y {len(file_list) - 5} archivos más\n"
        
        return [types.TextContent(type="text", text=report)]
        
    except Exception as e:
        logger.error(f"Error analizando descargas: {e}")
        return [types.TextContent(
            type="text",
            text=f"[ERROR] Error al analizar: {str(e)}"
        )]

async def organize_files(dry_run: bool, categories: Optional[List[str]] = None) -> list[types.TextContent]:
    """Organiza los archivos en carpetas por categoría"""
    try:
        if not DOWNLOADS_FOLDER.exists():
            return [types.TextContent(
                type="text",
                text=f"[ERROR] La carpeta de descargas no existe: {DOWNLOADS_FOLDER}"
            )]
        
        files = [f for f in DOWNLOADS_FOLDER.iterdir() if f.is_file()]
        
        if not files:
            return [types.TextContent(
                type="text",
                text="[INFO] No hay archivos para organizar"
            )]
        
        moved_files = []
        errors = []
        
        for file_path in files:
            try:
                category = get_file_category(file_path.suffix)
                
                # Filtrar por categorías si se especificaron
                if categories and category not in categories:
                    continue
                
                target_folder = get_target_folder(file_path)
                target_path = target_folder / file_path.name
                
                # Verificar si el archivo ya existe en destino
                if target_path.exists():
                    # Generar nombre único
                    counter = 1
                    stem = file_path.stem
                    suffix = file_path.suffix
                    while target_path.exists():
                        new_name = f"{stem}_{counter}{suffix}"
                        target_path = target_folder / new_name
                        counter += 1
                
                if not dry_run:
                    # Crear carpeta si no existe
                    target_folder.mkdir(parents=True, exist_ok=True)
                    
                    # Mover archivo
                    shutil.move(str(file_path), str(target_path))
                
                moved_files.append({
                    "original": str(file_path),
                    "target": str(target_path),
                    "category": category
                })
                
            except Exception as e:
                errors.append(f"Error con {file_path.name}: {str(e)}")
        
        # Generar reporte
        mode_text = "[SIMULACIÓN]" if dry_run else "[EJECUTADO]"
        report = f"[ORGANIZACIÓN] Archivos - {mode_text}\n\n"
        
        if moved_files:
            report += f"Archivos procesados: {len(moved_files)}\n\n"
            
            # Agrupar por categoría
            by_category = {}
            for file_info in moved_files:
                cat = file_info["category"]
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(file_info)
            
            for category, files_in_cat in by_category.items():
                report += f"{category} ({len(files_in_cat)} archivos):\n"
                for file_info in files_in_cat[:3]:  # Mostrar solo los primeros 3
                    original_name = Path(file_info["original"]).name
                    report += f"  • {original_name}\n"
                if len(files_in_cat) > 3:
                    report += f"  ... y {len(files_in_cat) - 3} archivos más\n"
                report += "\n"
        
        if errors:
            report += f"[ERRORES] ({len(errors)}):\n"
            for error in errors[:5]:  # Mostrar solo los primeros 5
                report += f"  • {error}\n"
            if len(errors) > 5:
                report += f"  ... y {len(errors) - 5} errores más\n"
        
        if dry_run and moved_files:
            report += "\n[TIP] Para ejecutar realmente, usa dry_run: false"
        
        return [types.TextContent(type="text", text=report)]
        
    except Exception as e:
        logger.error(f"Error organizando archivos: {e}")
        return [types.TextContent(
            type="text",
            text=f"[ERROR] Error al organizar: {str(e)}"
        )]

async def create_folder_structure(base_folder: str) -> list[types.TextContent]:
    """Crea la estructura de carpetas para organización"""
    try:
        base_path = Path(base_folder)
        organized_path = base_path / "Organizados"
        
        created_folders = []
        
        for category, config in FILE_ORGANIZATION.items():
            folder_path = organized_path / category
            folder_path.mkdir(parents=True, exist_ok=True)
            created_folders.append(f"{category}")
        
        report = f"[ESTRUCTURA] Carpetas creadas\n\n"
        report += f"Ubicación: {organized_path}\n\n"
        report += "Carpetas creadas:\n"
        
        for folder in created_folders:
            report += f"  • {folder}\n"
        
        return [types.TextContent(type="text", text=report)]
        
    except Exception as e:
        logger.error(f"Error creando estructura: {e}")
        return [types.TextContent(
            type="text",
            text=f"[ERROR] Error al crear estructura: {str(e)}"
        )]

async def get_file_info(filename: str) -> list[types.TextContent]:
    """Obtiene información detallada de un archivo"""
    try:
        file_path = DOWNLOADS_FOLDER / filename
        
        if not file_path.exists():
            return [types.TextContent(
                type="text",
                text=f"[ERROR] Archivo no encontrado: {filename}"
            )]
        
        stat = file_path.stat()
        category = get_file_category(file_path.suffix)
        target_folder = get_target_folder(file_path)
        
        report = f"[ARCHIVO] Información detallada\n\n"
        report += f"Nombre: {file_path.name}\n"
        report += f"Ubicación: {file_path.parent}\n"
        report += f"Categoría: {category}\n"
        report += f"Tamaño: {round(stat.st_size / (1024 * 1024), 2)} MB\n"
        report += f"Modificado: {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Destino sugerido: {target_folder}\n"
        
        return [types.TextContent(type="text", text=report)]
        
    except Exception as e:
        logger.error(f"Error obteniendo info del archivo: {e}")
        return [types.TextContent(
            type="text",
            text=f"[ERROR] Error al obtener información: {str(e)}"
        )]

async def cleanup_empty_folders(dry_run: bool) -> list[types.TextContent]:
    """Elimina carpetas vacías"""
    try:
        organized_path = DOWNLOADS_FOLDER / "Organizados"
        
        if not organized_path.exists():
            return [types.TextContent(
                type="text",
                text="[ERROR] No existe la carpeta 'Organizados'"
            )]
        
        empty_folders = []
        
        # Buscar carpetas vacías
        for folder in organized_path.rglob("*"):
            if folder.is_dir() and not any(folder.iterdir()):
                empty_folders.append(folder)
                if not dry_run:
                    folder.rmdir()
        
        mode_text = "[SIMULACIÓN]" if dry_run else "[EJECUTADO]"
        report = f"[LIMPIEZA] Carpetas vacías - {mode_text}\n\n"
        
        if empty_folders:
            report += f"Carpetas vacías encontradas: {len(empty_folders)}\n\n"
            for folder in empty_folders[:10]:  # Mostrar solo las primeras 10
                relative_path = folder.relative_to(organized_path)
                report += f"  • {relative_path}\n"
            if len(empty_folders) > 10:
                report += f"  ... y {len(empty_folders) - 10} carpetas más\n"
                
            if dry_run:
                report += "\n[TIP] Para ejecutar realmente, usa dry_run: false"
        else:
            report += "[OK] No se encontraron carpetas vacías"
        
        return [types.TextContent(type="text", text=report)]
        
    except Exception as e:
        logger.error(f"Error en limpieza: {e}")
        return [types.TextContent(
            type="text",
            text=f"[ERROR] Error en limpieza: {str(e)}"
        )]

async def main():
    """Función principal para ejecutar el servidor"""
    # Configurar stdio transport
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    print("[INFO] Iniciando servidor MCP para organización de archivos...")
    print("[INFO] Conecta desde Claude u otro cliente MCP")
    print("[INFO] Presiona Ctrl+C para terminar")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Servidor MCP detenido")
    except Exception as e:
        print(f"[ERROR] Error en servidor MCP: {e}")
        import traceback
        traceback.print_exc()