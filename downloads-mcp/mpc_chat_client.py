"""
Cliente MCP interactivo tipo chat
Permite usar el MCP como si fuera una conversación natural
Perfecto para demostraciones en clase
"""

import asyncio
import json
import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime

# Importar funciones del servidor MCP directamente
from file_organizer_server import (
    analyze_downloads, organize_files, create_folder_structure,
    get_file_info, cleanup_empty_folders
)
from config import DOWNLOADS_FOLDER, FILE_ORGANIZATION

class MCPChatClient:
    """Cliente MCP que simula una conversación tipo chat"""
    
    def __init__(self):
        self.use_uv = self.check_uv()
        self.conversation_history = []
        self.commands = {
            'analizar': self.cmd_analyze,
            'analisis': self.cmd_analyze,
            'analyze': self.cmd_analyze,
            'ver': self.cmd_analyze,
            'mostrar': self.cmd_analyze,
            
            'organizar': self.cmd_organize,
            'organize': self.cmd_organize,
            'ordenar': self.cmd_organize,
            'limpiar': self.cmd_organize,
            
            'estructura': self.cmd_structure,
            'carpetas': self.cmd_structure,
            'folders': self.cmd_structure,
            'crear': self.cmd_structure,
            
            'info': self.cmd_file_info,
            'informacion': self.cmd_file_info,
            'detalles': self.cmd_file_info,
            'archivo': self.cmd_file_info,
            
            'limpiar_vacias': self.cmd_cleanup,
            'cleanup': self.cmd_cleanup,
            'vacias': self.cmd_cleanup,
            
            'ayuda': self.cmd_help,
            'help': self.cmd_help,
            'comandos': self.cmd_help,
            '?': self.cmd_help,
            
            'salir': self.cmd_exit,
            'exit': self.cmd_exit,
            'quit': self.cmd_exit,
            'bye': self.cmd_exit,
        }
    
    def check_uv(self):
        """Verifica si UV está disponible"""
        try:
            subprocess.run(["uv", "--version"], capture_output=True, check=True)
            return True
        except:
            return False
    
    def safe_print(self, text, prefix="[CLAUDE]"):
        """Impresión segura con prefijo tipo chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        try:
            print(f"{prefix} [{timestamp}] {text}")
        except UnicodeEncodeError:
            print(f"{prefix} [{timestamp}] {text.encode('ascii', 'replace').decode('ascii')}")
    
    def print_user_input(self, text):
        """Muestra la entrada del usuario"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[TU] [{timestamp}] {text}")
    
    def parse_command(self, user_input):
        """Analiza la entrada del usuario y determina qué comando ejecutar"""
        user_input = user_input.lower().strip()
        
        # Palabras clave para diferentes comandos
        for keyword, command_func in self.commands.items():
            if keyword in user_input:
                return command_func, user_input
        
        # Si no encuentra comando específico, ofrecer ayuda
        return self.cmd_help, user_input
    
    async def cmd_analyze(self, user_input):
        """Comando para analizar archivos"""
        self.safe_print("Analizando tu carpeta de descargas...")
        
        # Determinar si mostrar detalles
        show_details = any(word in user_input for word in ['detalle', 'completo', 'todo', 'full'])
        
        try:
            result = await analyze_downloads(show_details=show_details)
            for content in result:
                # Formatear la salida para que parezca más conversacional
                text = content.text
                self.safe_print("Aquí tienes el análisis de tu carpeta:")
                print("   " + text.replace('\n', '\n   '))
                
            # Sugerir próximos pasos
            self.safe_print("¿Qué te gustaría hacer ahora?")
            self.safe_print("- 'organizar' para organizar los archivos")
            self.safe_print("- 'estructura' para crear carpetas")
            self.safe_print("- 'info archivo.pdf' para ver detalles de un archivo")
            
        except Exception as e:
            self.safe_print(f"Error al analizar: {e}")
    
    async def cmd_organize(self, user_input):
        """Comando para organizar archivos"""
        # Determinar si es simulación o real
        is_simulation = any(word in user_input for word in ['simular', 'simulacion', 'prueba', 'test', 'preview'])
        dry_run = is_simulation or 'real' not in user_input
        
        # Determinar categorías específicas
        categories = None
        category_matches = []
        for category in FILE_ORGANIZATION.keys():
            if category.lower() in user_input:
                category_matches.append(category)
        
        if category_matches:
            categories = category_matches
        
        mode_text = "simulación" if dry_run else "organización REAL"
        self.safe_print(f"Iniciando {mode_text} de archivos...")
        
        if not dry_run:
            self.safe_print("¡ATENCIÓN! Esto MOVERÁ archivos realmente.")
            response = input("¿Estás seguro? (escribe 'SI' para confirmar): ")
            if response.upper() != 'SI':
                self.safe_print("Organización cancelada. Usa 'organizar simular' para ver qué pasaría.")
                return
        
        try:
            result = await organize_files(dry_run=dry_run, categories=categories)
            for content in result:
                text = content.text
                self.safe_print("Resultado de la organización:")
                print("   " + text.replace('\n', '\n   '))
                
            if dry_run:
                self.safe_print("Esto fue solo una simulación. Para organizar realmente, usa 'organizar real'")
            else:
                self.safe_print("¡Organización completada! Tus archivos han sido movidos.")
                
        except Exception as e:
            self.safe_print(f"Error al organizar: {e}")
    
    async def cmd_structure(self, user_input):
        """Comando para crear estructura de carpetas"""
        self.safe_print("Creando estructura de carpetas organizadas...")
        
        try:
            result = await create_folder_structure(str(DOWNLOADS_FOLDER))
            for content in result:
                text = content.text
                self.safe_print("Estructura creada:")
                print("   " + text.replace('\n', '\n   '))
                
            self.safe_print("¡Listo! Ahora puedes usar 'organizar' para mover los archivos.")
            
        except Exception as e:
            self.safe_print(f"Error creando estructura: {e}")
    
    async def cmd_file_info(self, user_input):
        """Comando para información de archivo específico"""
        # Extraer nombre de archivo del input
        words = user_input.split()
        filename = None
        
        # Buscar algo que parezca un nombre de archivo
        for word in words:
            if '.' in word and len(word) > 3:  # Probablemente un archivo
                filename = word
                break
        
        if not filename:
            self.safe_print("¿Qué archivo quieres que analice? Ejemplo: 'info archivo.pdf'")
            return
        
        self.safe_print(f"Obteniendo información de: {filename}")
        
        try:
            result = await get_file_info(filename)
            for content in result:
                text = content.text
                self.safe_print("Información del archivo:")
                print("   " + text.replace('\n', '\n   '))
                
        except Exception as e:
            self.safe_print(f"Error obteniendo info: {e}")
            self.safe_print("¿Existe el archivo? Usa 'analizar' para ver todos los archivos disponibles.")
    
    async def cmd_cleanup(self, user_input):
        """Comando para limpiar carpetas vacías"""
        dry_run = 'real' not in user_input
        
        mode_text = "simulando limpieza" if dry_run else "limpiando REALMENTE"
        self.safe_print(f"Iniciando {mode_text} de carpetas vacías...")
        
        try:
            result = await cleanup_empty_folders(dry_run=dry_run)
            for content in result:
                text = content.text
                self.safe_print("Resultado de la limpieza:")
                print("   " + text.replace('\n', '\n   '))
                
        except Exception as e:
            self.safe_print(f"Error en limpieza: {e}")
    
    async def cmd_help(self, user_input):
        """Muestra ayuda de comandos"""
        help_text = """
¡Hola! Soy tu asistente MCP para organizar archivos. Aquí tienes lo que puedo hacer:

COMANDOS PRINCIPALES:
• 'analizar' - Ver qué archivos tienes y cómo se clasificarían
• 'organizar' - Organizar archivos por categorías
• 'estructura' - Crear carpetas organizadas
• 'info archivo.pdf' - Ver detalles de un archivo específico
• 'limpiar vacias' - Eliminar carpetas vacías

MODIFICADORES:
• 'analizar completo' - Análisis con más detalles
• 'organizar simular' - Ver qué pasaría SIN mover archivos
• 'organizar real' - MOVER archivos realmente
• 'organizar documentos' - Solo organizar una categoría

EJEMPLOS DE USO:
• "analiza mi carpeta completo"
• "organizar solo imágenes en simulación"
• "crear estructura de carpetas"
• "info Django.rar"
• "limpiar carpetas vacías real"

OTROS COMANDOS:
• 'ayuda' - Mostrar esta ayuda
• 'salir' - Terminar el chat

Tu carpeta actual: """ + str(DOWNLOADS_FOLDER)
        
        self.safe_print(help_text)
    
    async def cmd_exit(self, user_input):
        """Termina el chat"""
        self.safe_print("¡Hasta luego! Ha sido un placer ayudarte a organizar tus archivos.")
        self.safe_print("Recuerda que siempre puedes volver ejecutando: uv run python mcp_chat_client.py")
        return False  # Señal para terminar el bucle
    
    def show_welcome(self):
        """Muestra mensaje de bienvenida"""
        print()
        print("=" * 70)
        print("   CHAT MCP - ORGANIZADOR DE ARCHIVOS")
        print("   Asistente inteligente para gestionar tu carpeta de descargas")
        print("=" * 70)
        print()
        
        self.safe_print("¡Hola! Soy tu asistente MCP para organizar archivos.")
        self.safe_print(f"Carpeta actual: {DOWNLOADS_FOLDER}")
        self.safe_print(f"Herramienta: {'UV (rápido)' if self.use_uv else 'Python tradicional'}")
        print()
        self.safe_print("Escribe 'analizar' para ver tus archivos, o 'ayuda' para ver todos los comandos.")
        self.safe_print("¡Vamos a organizar tu carpeta!")
        print()
    
    async def run_chat(self):
        """Ejecuta el bucle principal del chat"""
        self.show_welcome()
        
        while True:
            try:
                # Solicitar entrada del usuario
                user_input = input("[TU] > ").strip()
                
                if not user_input:
                    continue
                
                self.print_user_input(user_input)
                
                # Agregar al historial
                self.conversation_history.append(("user", user_input))
                
                # Parsear y ejecutar comando
                command_func, parsed_input = self.parse_command(user_input)
                result = await command_func(parsed_input)
                
                # Si el comando retorna False, terminar
                if result is False:
                    break
                
                print()  # Línea en blanco para separar
                
            except KeyboardInterrupt:
                print()
                self.safe_print("Chat interrumpido. ¡Hasta luego!")
                break
            except EOFError:
                print()
                self.safe_print("¡Hasta luego!")
                break
            except Exception as e:
                self.safe_print(f"Error inesperado: {e}")
                self.safe_print("Escribe 'ayuda' para ver los comandos disponibles.")

async def main():
    """Función principal"""
    client = MCPChatClient()
    await client.run_chat()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[ERROR] Error fatal: {e}")
        print("[TIP] Asegúrate de tener las dependencias instaladas: uv add mcp pydantic")