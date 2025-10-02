"""
Demostración completa del MCP Organizador de Archivos
Incluye creación de archivos de prueba y simulación de uso real
Version sin emojis - compatible con cualquier codificacion
"""

import asyncio
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import time

# Importar configuración
from config import DOWNLOADS_FOLDER, FILE_ORGANIZATION

class CompleteMCPDemo:
    """Demostración completa del MCP"""
    
    def __init__(self):
        self.downloads_folder = DOWNLOADS_FOLDER
        self.use_uv = self.check_uv()
        self.demo_files = []
        
    def check_uv(self):
        """Verifica si UV está disponible"""
        try:
            subprocess.run(["uv", "--version"], capture_output=True, check=True)
            return True
        except:
            return False
    
    def safe_print(self, text, delay=0.5):
        """Impresión segura sin emojis"""
        try:
            print(text)
        except UnicodeEncodeError:
            print(text.encode('ascii', 'replace').decode('ascii'))
        
        if delay > 0:
            time.sleep(delay)
    
    def create_demo_files(self):
        """Crea archivos de demostración en la carpeta de descargas"""
        self.safe_print("\n[DEMO] CREANDO ARCHIVOS DE DEMOSTRACIÓN")
        self.safe_print("=" * 40)
        
        # Asegurar que existe la carpeta de descargas
        self.downloads_folder.mkdir(exist_ok=True)
        
        # Archivos de demostración con contenido
        demo_files_data = [
            # Documentos
            ("Informe_Proyecto_2024.pdf", "Documento PDF simulado para la demostración"),
            ("Presentacion_MCP.docx", "Presentación sobre Model Context Protocol"),
            ("Notas_Clase.txt", "Notas importantes para la clase de programación"),
            ("Manual_Usuario.rtf", "Manual de usuario del sistema MCP"),
            
            # Imágenes
            ("screenshot_demo.png", "Captura de pantalla de la demostración"),
            ("logo_proyecto.jpg", "Logo del proyecto MCP organizador"),
            ("diagrama_flujo.svg", "Diagrama de flujo del proceso"),
            
            # Videos
            ("video_explicativo.mp4", "Video explicativo del proyecto"),
            ("demo_funcionamiento.avi", "Demostración del funcionamiento"),
            
            # Audio
            ("audio_presentacion.mp3", "Audio de la presentación"),
            ("podcast_tecnologia.wav", "Podcast sobre tecnología"),
            
            # Programación
            ("script_backup.py", "# Script de backup automático\nprint('Hola mundo')"),
            ("estilos_web.css", "/* Estilos CSS para la web */\nbody { margin: 0; }"),
            ("configuracion.json", '{"version": "1.0", "autor": "Estudiante"}'),
            
            # Comprimidos y ejecutables
            ("archivo_comprimido.zip", "Archivo ZIP simulado"),
            ("instalador_programa.exe", "Instalador simulado"),
            
            # Hojas de cálculo
            ("datos_proyecto.xlsx", "Datos importantes del proyecto"),
            ("presupuesto.csv", "Presupuesto del proyecto"),
            
            # Archivos diversos
            ("archivo_desconocido.xyz", "Archivo de tipo desconocido"),
            ("temp_download.tmp", "Archivo temporal de descarga"),
        ]
        
        created_count = 0
        for filename, content in demo_files_data:
            file_path = self.downloads_folder / filename
            
            # Solo crear si no existe
            if not file_path.exists():
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.demo_files.append(filename)
                    created_count += 1
                    self.safe_print(f"  [FILE] Creado: {filename}", 0.1)
                except Exception as e:
                    self.safe_print(f"  [ERROR] Error creando {filename}: {e}")
            else:
                self.safe_print(f"  [OK] Ya existe: {filename}", 0.1)
        
        self.safe_print(f"\n[SUCCESS] Archivos de demostración listos: {created_count} creados")
        total_files = len([f for f in self.downloads_folder.iterdir() if f.is_file()])
        self.safe_print(f"[STATS] Total de archivos en descargas: {total_files}")
    
    def get_python_command(self):
        """Obtiene el comando correcto de Python"""
        if self.use_uv:
            return ["uv", "run", "python"]
        else:
            return [sys.executable]
    
    async def demo_analyze(self):
        """Demostración del análisis de archivos"""
        self.safe_print("\n[ANALYZE] DEMOSTRACIÓN: Análisis de archivos")
        self.safe_print("-" * 40)
        
        python_cmd = self.get_python_command()
        
        try:
            # Simular llamada a la herramienta analyze_downloads
            demo_script = '''
import sys
import os
sys.path.append('.')

# Importar funciones necesarias
from file_organizer_server import analyze_downloads

# Ejecutar análisis
import asyncio
async def run_demo():
    result = await analyze_downloads(show_details=True)
    for content in result:
        print(content.text)

asyncio.run(run_demo())
'''
            
            with open("temp_demo_analyze.py", "w", encoding='utf-8') as f:
                f.write(demo_script)
            
            self.safe_print("[TOOL] Ejecutando análisis de archivos...")
            result = subprocess.run(
                python_cmd + ["temp_demo_analyze.py"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                self.safe_print("[OK] Análisis completado:")
                self.safe_print(result.stdout)
            else:
                self.safe_print("[ERROR] Error en análisis:")
                self.safe_print(result.stderr)
            
            # Limpiar archivo temporal
            Path("temp_demo_analyze.py").unlink(missing_ok=True)
            
        except Exception as e:
            self.safe_print(f"[ERROR] Error en demostración de análisis: {e}")
    
    async def demo_create_structure(self):
        """Demostración de creación de estructura"""
        self.safe_print("\n[BUILD] DEMOSTRACIÓN: Creación de estructura")
        self.safe_print("-" * 42)
        
        python_cmd = self.get_python_command()
        
        try:
            demo_script = '''
import sys
sys.path.append('.')

from file_organizer_server import create_folder_structure
from config import DOWNLOADS_FOLDER

import asyncio
async def run_demo():
    result = await create_folder_structure(str(DOWNLOADS_FOLDER))
    for content in result:
        print(content.text)

asyncio.run(run_demo())
'''
            
            with open("temp_demo_structure.py", "w", encoding='utf-8') as f:
                f.write(demo_script)
            
            self.safe_print("[TOOL] Creando estructura de carpetas...")
            result = subprocess.run(
                python_cmd + ["temp_demo_structure.py"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                self.safe_print("[OK] Estructura creada:")
                self.safe_print(result.stdout)
            else:
                self.safe_print("[ERROR] Error creando estructura:")
                self.safe_print(result.stderr)
            
            Path("temp_demo_structure.py").unlink(missing_ok=True)
            
        except Exception as e:
            self.safe_print(f"[ERROR] Error en demostración de estructura: {e}")
    
    async def demo_organize_dry_run(self):
        """Demostración de organización en modo simulación"""
        self.safe_print("\n[TARGET] DEMOSTRACIÓN: Organización (simulación)")
        self.safe_print("-" * 43)
        
        python_cmd = self.get_python_command()
        
        try:
            demo_script = '''
import sys
sys.path.append('.')

from file_organizer_server import organize_files

import asyncio
async def run_demo():
    result = await organize_files(dry_run=True, categories=None)
    for content in result:
        print(content.text)

asyncio.run(run_demo())
'''
            
            with open("temp_demo_organize.py", "w", encoding='utf-8') as f:
                f.write(demo_script)
            
            self.safe_print("[TOOL] Simulando organización de archivos...")
            result = subprocess.run(
                python_cmd + ["temp_demo_organize.py"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                self.safe_print("[OK] Simulación completada:")
                self.safe_print(result.stdout)
            else:
                self.safe_print("[ERROR] Error en simulación:")
                self.safe_print(result.stderr)
            
            Path("temp_demo_organize.py").unlink(missing_ok=True)
            
        except Exception as e:
            self.safe_print(f"[ERROR] Error en demostración de organización: {e}")
    
    async def demo_file_info(self):
        """Demostración de información de archivo"""
        self.safe_print("\n[FILE] DEMOSTRACIÓN: Información de archivo")
        self.safe_print("-" * 40)
        
        # Buscar un archivo de ejemplo
        files = [f for f in self.downloads_folder.iterdir() if f.is_file()]
        if not files:
            self.safe_print("[ERROR] No hay archivos para analizar")
            return
        
        example_file = files[0].name
        self.safe_print(f"[TARGET] Analizando archivo: {example_file}")
        
        python_cmd = self.get_python_command()
        
        try:
            demo_script = f'''
import sys
sys.path.append('.')

from file_organizer_server import get_file_info

import asyncio
async def run_demo():
    result = await get_file_info("{example_file}")
    for content in result:
        print(content.text)

asyncio.run(run_demo())
'''
            
            with open("temp_demo_fileinfo.py", "w", encoding='utf-8') as f:
                f.write(demo_script)
            
            result = subprocess.run(
                python_cmd + ["temp_demo_fileinfo.py"],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                self.safe_print("[OK] Información obtenida:")
                self.safe_print(result.stdout)
            else:
                self.safe_print("[ERROR] Error obteniendo información:")
                self.safe_print(result.stderr)
            
            Path("temp_demo_fileinfo.py").unlink(missing_ok=True)
            
        except Exception as e:
            self.safe_print(f"[ERROR] Error en demostración de info: {e}")
    
    def show_mcp_explanation(self):
        """Explicación del MCP para la clase"""
        self.safe_print("\n[CLASS] EXPLICACIÓN PARA LA CLASE")
        self.safe_print("=" * 30)
        
        explanation = """
[TARGET] ¿QUÉ ES MCP (Model Context Protocol)?

MCP es un protocolo que permite a los modelos de IA (como Claude) 
interactuar con herramientas externas y sistemas.

[TOOL] COMPONENTES PRINCIPALES:

1. SERVIDOR MCP (file_organizer_server.py):
   - Define las herramientas disponibles
   - Implementa la lógica de cada herramienta
   - Se comunica con el cliente a través de JSON-RPC

2. CLIENTE MCP (Claude en nuestro caso):
   - Conecta con el servidor
   - Llama a las herramientas según necesidades
   - Procesa las respuestas

3. HERRAMIENTAS (Tools):
   - Funciones específicas que puede ejecutar
   - Cada una tiene parámetros de entrada definidos
   - Retornan resultados estructurados

[FLOW] FLUJO DE TRABAJO:
   Usuario → Claude → Servidor MCP → Ejecuta herramienta → Retorna resultado → Claude → Usuario

[TIP] VENTAJAS:
   - Extensibilidad: Fácil agregar nuevas herramientas
   - Estandarización: Protocolo común para cualquier IA
   - Seguridad: Control sobre qué puede hacer la IA
   - Modularidad: Cada herramienta es independiente

[START] APLICACIONES REALES:
   - Automatización de tareas
   - Gestión de archivos
   - Acceso a bases de datos
   - Integración con APIs
   - Análisis de datos
"""
        
        for line in explanation.split('\n'):
            if line.strip():
                self.safe_print(line.strip(), 0.3)
    
    def show_next_steps(self):
        """Muestra los próximos pasos"""
        self.safe_print("\n[SHOW] PRÓXIMOS PASOS PARA LA DEMOSTRACIÓN")
        self.safe_print("=" * 40)
        
        steps = [
            "1. Ejecutar servidor MCP:",
            f"   {'uv run python' if self.use_uv else 'python'} file_organizer_server.py",
            "",
            "2. Conectar desde Claude:",
            "   - El servidor estará esperando conexiones",
            "   - Claude puede usar las 5 herramientas disponibles",
            "",
            "3. Herramientas disponibles:",
            "   • analyze_downloads - Analizar archivos",
            "   • organize_files - Organizar por categorías", 
            "   • create_folder_structure - Crear estructura",
            "   • get_file_info - Info de archivo específico",
            "   • cleanup_empty_folders - Limpiar carpetas vacías",
            "",
            "4. Personalizar para tu clase:",
            "   - Editar config.py para nuevas categorías",
            "   - Agregar nuevas herramientas en el servidor",
            "   - Crear diferentes tipos de archivos de prueba",
            "",
            "5. Conceptos a explicar:",
            "   - JSON-RPC para comunicación",
            "   - Stdin/stdout para transporte",
            "   - Schemas para validación de parámetros",
            "   - Async/await para operaciones concurrentes"
        ]
        
        for step in steps:
            self.safe_print(step, 0.2)
    
    def cleanup_demo_files(self):
        """Ofrece limpiar archivos de demostración"""
        self.safe_print("\n[CLEAN] ¿Limpiar archivos de demostración?")
        
        try:
            response = input("¿Eliminar archivos creados para la demo? (s/n): ").lower()
            
            if response in ['s', 'sí', 'si', 'y', 'yes']:
                deleted_count = 0
                for filename in self.demo_files:
                    file_path = self.downloads_folder / filename
                    if file_path.exists():
                        file_path.unlink()
                        deleted_count += 1
                        self.safe_print(f"  [DELETE] Eliminado: {filename}")
                
                self.safe_print(f"\n[CLEAN] Archivos eliminados: {deleted_count}")
            else:
                self.safe_print("[FOLDER] Archivos de demostración conservados")
                
        except KeyboardInterrupt:
            self.safe_print("\n[FOLDER] Archivos de demostración conservados")
    
    async def run_complete_demo(self):
        """Ejecuta la demostración completa"""
        self.safe_print("[SHOW] DEMOSTRACIÓN COMPLETA - MCP ORGANIZADOR DE ARCHIVOS")
        self.safe_print("=" * 55)
        
        self.safe_print(f"[TOOL] Herramienta: {'UV (rápido)' if self.use_uv else 'Python tradicional'}")
        self.safe_print(f"[FOLDER] Carpeta objetivo: {self.downloads_folder}")
        
        # Explicación inicial
        self.show_mcp_explanation()
        
        # Crear archivos de demostración
        self.create_demo_files()
        
        # Demostrar todas las herramientas
        await self.demo_analyze()
        await self.demo_create_structure()
        await self.demo_file_info()
        await self.demo_organize_dry_run()
        
        # Próximos pasos
        self.show_next_steps()
        
        # Limpiar
        self.cleanup_demo_files()
        
        self.safe_print("\n[SUCCESS] ¡DEMOSTRACIÓN COMPLETA FINALIZADA!")
        self.safe_print("[CLASS] ¡Lista para explicar en tu clase!")

async def main():
    """Función principal"""
    demo = CompleteMCPDemo()
    await demo.run_complete_demo()

if __name__ == "__main__":
    asyncio.run(main())