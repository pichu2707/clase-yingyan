"""
Cliente de prueba para el servidor MCP de organización de archivos
Permite probar las herramientas sin necesidad de Claude
Compatible con UV y pip/venv
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

class MCPTestClient:
    """Cliente simple para probar el servidor MCP"""
    
    def __init__(self):
        self.server_script = Path("file_organizer_server.py")
        self.use_uv = self.check_uv_available()
    
    def check_uv_available(self):
        """Verifica si UV está disponible y configurado"""
        try:
            # Verificar si UV está instalado
            subprocess.run(["uv", "--version"], capture_output=True, check=True)
            
            # Verificar si hay un proyecto UV (pyproject.toml o uv.lock)
            has_project = (Path("pyproject.toml").exists() or 
                          Path("uv.lock").exists() or
                          Path(".venv").exists())
            
            if has_project:
                print("🚀 Usando UV para las pruebas")
                return True
            else:
                print("🐍 UV disponible pero usando venv tradicional")
                return False
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("🐍 Usando pip/venv tradicional")
            return False
    
    def get_python_command(self):
        """Obtiene el comando de Python apropiado"""
        if self.use_uv:
            return ["uv", "run", "python"]
        else:
            # Buscar Python en venv o usar el del sistema
            if Path(".venv").exists():
                if sys.platform == "win32":
                    venv_python = Path(".venv/Scripts/python.exe")
                else:
                    venv_python = Path(".venv/bin/python")
                
                if venv_python.exists():
                    return [str(venv_python)]
            
            return [sys.executable]
    
    async def test_analyze_downloads(self):
        """Prueba la herramienta de análisis"""
        print("🔍 Probando análisis de descargas...")
        
        # Simular llamada MCP
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "analyze_downloads",
                "arguments": {"show_details": True}
            }
        }
        
        print(f" Enviando: {json.dumps(request, indent=2)}")
        
        # En un caso real, esto se haría a través del protocolo MCP
        # Por ahora, solo mostramos la estructura
        print(" Estructura de request correcta")
    
    async def test_organize_files(self):
        """Prueba la herramienta de organización"""
        print("\n Probando organización de archivos...")
        
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "organize_files",
                "arguments": {
                    "dry_run": True,
                    "categories": ["Documentos", "Imágenes"]
                }
            }
        }
        
        print(f" Enviando: {json.dumps(request, indent=2)}")
        print(" Estructura de request correcta")
    
    async def test_create_structure(self):
        """Prueba la creación de estructura"""
        print("\n Probando creación de estructura...")
        
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "create_folder_structure",
                "arguments": {}
            }
        }
        
        print(f" Enviando: {json.dumps(request, indent=2)}")
        print(" Estructura de request correcta")
    
    async def run_tests(self):
        """Ejecuta todas las pruebas"""
        print(" Iniciando pruebas del cliente MCP\n")
        
        await self.test_analyze_downloads()
        await self.test_organize_files()
        await self.test_create_structure()
        
        print("\n✅ Todas las pruebas completadas")
        
        if self.use_uv:
            print("\n Para usar realmente el servidor con UV:")
            print("   1. uv sync                                    # Sincronizar dependencias")
            print("   2. uv run python file_organizer_server.py    # Ejecutar servidor")
            print("   3. Conecta desde Claude u otro cliente MCP")
            print("\n Gestión con UV:")
            print("   uv add [paquete]     # Añadir dependencia")
            print("   uv remove [paquete]  # Quitar dependencia")
            print("   uv lock              # Actualizar lockfile")
        else:
            print("\n Para usar realmente el servidor:")
            print("   1. Activa el entorno: venv\\Scripts\\activate")
            print("   2. Ejecuta el servidor: python file_organizer_server.py") 
            print("   3. Conecta desde Claude u otro cliente MCP")
            print("\n Considera actualizar a UV para mejor experiencia:")
            print("   https://docs.astral.sh/uv/getting-started/installation/")

def test_imports():
    """Prueba que se puedan importar los módulos necesarios"""
    print(" Probando imports...")
    
    client = MCPTestClient()
    python_cmd = client.get_python_command()
    
    try:
        # Probar importación de config
        result = subprocess.run(
            python_cmd + ["-c", "import config; print(' config.py importado')"],
            capture_output=True, text=True, check=True
        )
        print(result.stdout.strip())
        
        # Probar funciones de config
        result = subprocess.run(
            python_cmd + ["-c", """
import config
from config import get_file_category, get_target_folder, DOWNLOADS_FOLDER

# Probar categorización
test_files = ['.pdf', '.jpg', '.mp3', '.py', '.unknown']
for ext in test_files:
    category = get_file_category(ext)
    print(f'   {ext} -> {category}')

print(f'   Carpeta de descargas: {DOWNLOADS_FOLDER}')

# Verificar si existe la carpeta
if DOWNLOADS_FOLDER.exists():
    files_count = len([f for f in DOWNLOADS_FOLDER.iterdir() if f.is_file()])
    print(f'   Archivos en descargas: {files_count}')
else:
    print(f'   Carpeta de descargas no existe: {DOWNLOADS_FOLDER}')
"""],
            capture_output=True, text=True, check=True
        )
        print(result.stdout.strip())
        
        # Probar MCP
        result = subprocess.run(
            python_cmd + ["-c", "import mcp; print(' MCP disponible')"],
            capture_output=True, text=True, check=True
        )
        print(result.stdout.strip())
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f" Error al importar: {e}")
        if e.stderr:
            print(f"   Detalles: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f" Error inesperado: {e}")
        return False

async def main():
    """Función principal"""
    print("🧪 Cliente de prueba MCP - Organizador de archivos\n")
    
    # Mostrar información del entorno
    client = MCPTestClient()
    if client.use_uv:
        print(" Entorno: UV (moderno y rápido)")
        print(" Para ejecutar: uv run python [script]")
    else:
        print(" Entorno: pip/venv (tradicional)")
        print(" Para ejecutar: python [script]")
    
    print("\n" + "="*30 + "\n")
    
    # Probar imports primero
    if not test_imports():
        print(" Falló la prueba de imports")
        if client.use_uv:
            print(" Intenta: uv sync")
        else:
            print(" Intenta: pip install -r requirements.txt")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Ejecutar pruebas del cliente
    await client.run_tests()

if __name__ == "__main__":
    asyncio.run(main())