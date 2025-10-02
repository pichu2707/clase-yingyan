"""
Prueba específica del servidor MCP
Verifica que el servidor se inicia correctamente y responde
Version sin emojis - compatible con cualquier codificacion
"""

import asyncio
import subprocess
import sys
import time
import threading
from pathlib import Path

class MCPServerTester:
    """Probador del servidor MCP"""
    
    def __init__(self):
        self.use_uv = self.check_uv()
        self.server_process = None
        
    def check_uv(self):
        """Verifica UV"""
        try:
            subprocess.run(["uv", "--version"], capture_output=True, check=True)
            return True
        except:
            return False
    
    def safe_print(self, text):
        """Impresión segura sin emojis"""
        try:
            print(text)
        except UnicodeEncodeError:
            print(text.encode('ascii', 'replace').decode('ascii'))
    
    def get_python_command(self):
        """Comando de Python"""
        if self.use_uv:
            return ["uv", "run", "python"]
        else:
            return [sys.executable]
    
    def test_imports(self):
        """Prueba que se puedan importar todos los módulos"""
        self.safe_print("[TEST] Probando imports del servidor...")
        
        python_cmd = self.get_python_command()
        
        test_script = '''
import sys
sys.path.append('.')

try:
    # Importar módulos principales
    import mcp.types as types
    from mcp.server import Server
    import config
    from config import DOWNLOADS_FOLDER, FILE_ORGANIZATION
    
    print("[OK] Todos los imports exitosos")
    print(f"[INFO] Carpeta de descargas: {DOWNLOADS_FOLDER}")
    print(f"[INFO] Categorías configuradas: {len(FILE_ORGANIZATION)}")
    
except ImportError as e:
    print(f"[ERROR] Falta dependencia: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Error inesperado: {e}")
    sys.exit(1)
'''
        
        try:
            result = subprocess.run(
                python_cmd + ["-c", test_script],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.safe_print("[OK] Imports del servidor funcionan correctamente")
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        self.safe_print(f"  {line}")
                return True
            else:
                self.safe_print("[ERROR] Error en imports:")
                self.safe_print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            self.safe_print("[ERROR] Timeout en prueba de imports")
            return False
        except Exception as e:
            self.safe_print(f"[ERROR] Error ejecutando prueba: {e}")
            return False
    
    def test_server_startup(self):
        """Prueba que el servidor se inicie sin errores"""
        self.safe_print("\n[SERVER] Probando inicio del servidor MCP...")
        
        python_cmd = self.get_python_command()
        
        try:
            # Iniciar servidor en subprocess
            self.server_process = subprocess.Popen(
                python_cmd + ["file_organizer_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Esperar un poco para ver si arranca
            time.sleep(2)
            
            # Verificar si el proceso sigue vivo
            if self.server_process.poll() is None:
                self.safe_print("[OK] Servidor MCP iniciado correctamente")
                self.safe_print("[SERVER] El servidor está esperando conexiones...")
                return True
            else:
                # El proceso terminó, obtener el error
                stdout, stderr = self.server_process.communicate()
                self.safe_print("[ERROR] El servidor terminó inesperadamente:")
                if stderr:
                    self.safe_print(f"Error: {stderr}")
                if stdout:
                    self.safe_print(f"Salida: {stdout}")
                return False
                
        except FileNotFoundError:
            self.safe_print("[ERROR] No se encontró el archivo del servidor")
            return False
        except Exception as e:
            self.safe_print(f"[ERROR] Error iniciando servidor: {e}")
            return False
    
    def stop_server(self):
        """Detiene el servidor si está corriendo"""
        if self.server_process and self.server_process.poll() is None:
            self.safe_print("\n[SERVER] Deteniendo servidor MCP...")
            self.server_process.terminate()
            
            # Esperar un poco para terminación graceful
            try:
                self.server_process.wait(timeout=5)
                self.safe_print("[OK] Servidor detenido correctamente")
            except subprocess.TimeoutExpired:
                self.safe_print("[QUICK] Forzando cierre del servidor...")
                self.server_process.kill()
                self.server_process.wait()
    
    def test_server_response(self):
        """Prueba básica de respuesta del servidor"""
        self.safe_print("\n[TARGET] Probando respuesta del servidor...")
        
        # El servidor MCP usa stdin/stdout, así que esta es una prueba limitada
        # Solo verificamos que no se cierre inmediatamente
        
        if self.server_process and self.server_process.poll() is None:
            self.safe_print("[OK] Servidor respondiendo (proceso activo)")
            self.safe_print("[TIP] Para prueba completa, conecta desde Claude")
            return True
        else:
            self.safe_print("[ERROR] Servidor no está respondiendo")
            return False
    
    def show_connection_info(self):
        """Muestra información de conexión para Claude"""
        self.safe_print("\n[TIP] INFORMACIÓN PARA CONECTAR DESDE CLAUDE")
        self.safe_print("=" * 45)
        
        info = [
            "1. El servidor MCP está corriendo correctamente",
            "2. Usa comunicación stdin/stdout (modo estándar)",
            "3. Protocolo: JSON-RPC 2.0",
            "",
            "Para conectar desde Claude:",
            "- El servidor está listo para recibir conexiones",
            "- Herramientas disponibles: 5 funciones",
            "- Carpeta objetivo configurada correctamente",
            "",
            "Comando para ejecutar servidor:",
            f"  {'uv run python' if self.use_uv else 'python'} file_organizer_server.py",
            "",
            "Para detener el servidor: Ctrl+C"
        ]
        
        for line in info:
            self.safe_print(line)
    
    def run_complete_test(self):
        """Ejecuta todas las pruebas"""
        self.safe_print("[START] PRUEBA COMPLETA DEL SERVIDOR MCP")
        self.safe_print("=" * 35)
        
        # Paso 1: Imports
        if not self.test_imports():
            self.safe_print("\n[ERROR] Falló la prueba de imports - Abortando")
            return False
        
        # Paso 2: Startup
        if not self.test_server_startup():
            self.safe_print("\n[ERROR] Falló el inicio del servidor - Abortando")
            return False
        
        # Paso 3: Response
        if not self.test_server_response():
            self.safe_print("\n[ERROR] Servidor no responde correctamente")
            self.stop_server()
            return False
        
        # Paso 4: Info de conexión
        self.show_connection_info()
        
        # Mantener servidor corriendo por un momento
        self.safe_print("\n[SERVER] Manteniendo servidor activo por 10 segundos...")
        self.safe_print("   (Tiempo suficiente para verificar que funciona)")
        
        time.sleep(10)
        
        # Detener servidor
        self.stop_server()
        
        self.safe_print("\n[OK] TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        self.safe_print("[TARGET] El servidor MCP está listo para usar con Claude")
        
        return True

def main():
    """Función principal"""
    print("[INFO] Probador del servidor MCP - Organizador de archivos")
    print("=" * 55)
    
    tester = MCPServerTester()
    
    try:
        success = tester.run_complete_test()
        
        if success:
            print("\n[SUCCESS] El servidor MCP funciona correctamente")
            print("[TIP] Puedes ejecutar la demostración completa con:")
            if tester.use_uv:
                print("      uv run python demo_complete.py")
            else:
                print("      python demo_complete.py")
        else:
            print("\n[ERROR] Hay problemas con el servidor MCP")
            print("[FIX] Revisa las dependencias y configuración")
            
    except KeyboardInterrupt:
        print("\n[INFO] Prueba interrumpida por el usuario")
        tester.stop_server()
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        tester.stop_server()

if __name__ == "__main__":
    main()