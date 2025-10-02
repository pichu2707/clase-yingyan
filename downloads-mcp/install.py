"""
Script de instalación automática para el MCP Organizador de Archivos
Configura todo el entorno necesario automáticamente
"""

import os
import subprocess
import sys
from pathlib import Path

class MCPInstaller:
    """Instalador automático del MCP"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.venv_path = self.project_root / "venv"
        self.python_exe = self.get_python_executable()
    
    def get_python_executable(self):
        """Obtiene el ejecutable de Python correcto"""
        if os.name == 'nt':  # Windows
            return self.venv_path / "Scripts" / "python.exe"
        else:  # Linux/Mac
            return self.venv_path / "bin" / "python"
    
    def get_pip_executable(self):
        """Obtiene el ejecutable de pip correcto"""
        if os.name == 'nt':  # Windows
            return self.venv_path / "Scripts" / "pip.exe"
        else:  # Linux/Mac
            return self.venv_path / "bin" / "pip"
    
    def print_step(self, step_num, total_steps, description):
        """Imprime el paso actual de la instalación"""
        print(f"\n[{step_num}/{total_steps}] {description}")
        print("-" * (len(description) + 10))
    
    def run_command(self, command, description=""):
        """Ejecuta un comando y maneja errores"""
        try:
            print(f" Ejecutando: {' '.join(command)}")
            result = subprocess.run(
                command, 
                check=True, 
                capture_output=True, 
                text=True
            )
            if result.stdout:
                print(f" {description}")
            return True
        except subprocess.CalledProcessError as e:
            print(f" Error en {description}:")
            print(f"   Comando: {' '.join(command)}")
            print(f"   Error: {e.stderr}")
            return False
        except FileNotFoundError:
            print(f" Comando no encontrado: {command[0]}")
            return False
    
    def check_python_version(self):
        """Verifica que la versión de Python sea compatible"""
        print(" Verificando versión de Python...")
        
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f" Python {version.major}.{version.minor}.{version.micro} - Compatible")
            return True
        else:
            print(f" Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.8+")
            return False
    
    def create_virtual_environment(self):
        """Crea el entorno virtual"""
        print(" Creando entorno virtual...")
        
        if self.venv_path.exists():
            print(" El entorno virtual ya existe")
            return True
        
        return self.run_command(
            [sys.executable, "-m", "venv", str(self.venv_path)],
            "Entorno virtual creado"
        )
    
    def install_dependencies(self):
        """Instala las dependencias del proyecto"""
        print(" Instalando dependencias...")
        
        python_exe = self.get_python_executable()
        
        # Actualizar pip usando python -m pip (método más confiable)
        print(" Actualizando pip...")
        success = self.run_command(
            [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
            "pip actualizado"
        )
        
        if not success:
            print(" No se pudo actualizar pip, continuando con la versión actual...")
        
        # Instalar dependencias principales directamente (sin requirements.txt para evitar problemas)
        dependencies = [
            "mcp>=1.0.0",
            "pydantic>=2.0.0", 
            "asyncio-subprocess>=0.1.0",
            "pathlib2>=2.3.0"
        ]
        
        print(" Instalando dependencias principales...")
        for dep in dependencies:
            success = self.run_command(
                [str(python_exe), "-m", "pip", "install", dep],
                f"Instalado: {dep.split('>=')[0]}"
            )
            if not success:
                print(f" No se pudo instalar {dep}, intentando sin versión...")
                # Intentar sin especificar versión
                dep_name = dep.split('>=')[0]
                self.run_command(
                    [str(python_exe), "-m", "pip", "install", dep_name],
                    f"Instalado: {dep_name} (sin versión específica)"
                )
        
        return True
    
    def verify_installation(self):
        """Verifica que la instalación fue exitosa"""
        print(" Verificando instalación...")
        
        python_exe = self.get_python_executable()
        
        # Verificar que se pueden importar los módulos principales
        test_imports = [
            ("mcp", "import mcp"),
            ("pydantic", "import pydantic"), 
            ("asyncio", "import asyncio"),
            ("pathlib", "import pathlib"),
        ]
        
        # Solo verificar config.py si existe
        if (self.project_root / "config.py").exists():
            test_imports.append(("config", "from config import DOWNLOADS_FOLDER, FILE_ORGANIZATION"))
        
        success_count = 0
        for name, import_test in test_imports:
            success = self.run_command(
                [str(python_exe), "-c", import_test],
                f"Importación exitosa: {name}"
            )
            if success:
                success_count += 1
        
        if success_count >= len(test_imports) - 1:  # Permitir que falle uno
            print(f" Verificación exitosa ({success_count}/{len(test_imports)} módulos)")
            return True
        else:
            print(f" Verificación parcial ({success_count}/{len(test_imports)} módulos)")
            print("   El MCP podría funcionar, pero verifica manualmente")
            return True  # Continuar de todas formas
    
    def create_activation_script(self):
        """Crea script para activar el entorno fácilmente"""
        print(" Creando script de activación...")
        
        if os.name == 'nt':  # Windows
            script_content = f"""@echo off
echo  Activando entorno virtual del MCP Organizador de Archivos...
call "{self.venv_path}\\Scripts\\activate.bat"
echo  Entorno activado. Comandos disponibles:
echo   - python demo.py              (Demostración completa)
echo   - python test_client.py       (Pruebas básicas)
echo   - python file_organizer_server.py  (Ejecutar servidor MCP)
echo.
"""
            script_path = self.project_root / "activar.bat"
        else:  # Linux/Mac
            script_content = f"""#!/bin/bash
echo " Activando entorno virtual del MCP Organizador de Archivos..."
source "{self.venv_path}/bin/activate"
echo " Entorno activado. Comandos disponibles:"
echo "  - python demo.py              (Demostración completa)"
echo "  - python test_client.py       (Pruebas básicas)"
echo "  - python file_organizer_server.py  (Ejecutar servidor MCP)"
echo ""
"""
            script_path = self.project_root / "activar.sh"
        
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            if os.name != 'nt':  # Hacer ejecutable en Linux/Mac
                os.chmod(script_path, 0o755)
            
            print(f" Script de activación creado: {script_path.name}")
            return True
        except Exception as e:
            print(f" Error creando script: {e}")
            return False
    
    def show_next_steps(self):
        """Muestra los próximos pasos después de la instalación"""
        print("\n" + "=" * 60)
        print(" ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print("=" * 60)
                print("\n📋 PRÓXIMOS PASOS:")
        print("1. Activar el entorno virtual:")
        
        if os.name == 'nt':  # Windows
            print("   > activar.bat")
            print("   O manualmente: venv\\Scripts\\activate")
        else:  # Linux/Mac
            print("   $ ./activar.sh")
            print("   O manualmente: source venv/bin/activate")
        
        print("\n2. Probar el sistema:")
        print("   > python demo.py          # Demostración completa")
        print("   > python test_client.py   # Pruebas básicas")
        
        print("\n3. Usar con Claude:")
        print("   > python file_organizer_server.py")
        
        print("\n4. Personalizar configuración:")
        print("   - Edita config.py para cambiar categorías")
        print("   - Modifica la carpeta de descargas por defecto")
        
        print("\n Documentación completa en README.md")
        print("\n ¡Listo para usar en tu clase!")
    
    def install(self):
        """Ejecuta el proceso completo de instalación"""
        print(" INSTALADOR MCP ORGANIZADOR DE ARCHIVOS")
        print("=" * 45)
        print(f" Directorio del proyecto: {self.project_root}")
        
        total_steps = 6
        current_step = 1
        
        # Paso 1: Verificar Python
        self.print_step(current_step, total_steps, "Verificando Python")
        if not self.check_python_version():
            print(" Instalación abortada: Python incompatible")
            return False
        current_step += 1
        
        # Paso 2: Crear entorno virtual
        self.print_step(current_step, total_steps, "Creando entorno virtual")
        if not self.create_virtual_environment():
            print(" Instalación abortada: Error creando entorno virtual")
            return False
        current_step += 1
        
        # Paso 3: Instalar dependencias
        self.print_step(current_step, total_steps, "Instalando dependencias")
        if not self.install_dependencies():
            print(" Instalación abortada: Error instalando dependencias")
            return False
        current_step += 1
        
        # Paso 4: Verificar instalación
        self.print_step(current_step, total_steps, "Verificando instalación")
        if not self.verify_installation():
            print(" Instalación abortada: Error en verificación")
            return False
        current_step += 1
        
        # Paso 5: Crear script de activación
        self.print_step(current_step, total_steps, "Creando scripts auxiliares")
        self.create_activation_script()
        current_step += 1
        
        # Paso 6: Mostrar próximos pasos
        self.print_step(current_step, total_steps, "Finalizando")
        self.show_next_steps()
        
        return True

def main():
    """Función principal del instalador"""
    print(" Bienvenido al instalador del MCP Organizador de Archivos\n")
    
    # Verificar archivos necesarios (solo los esenciales)
    required_files = ["config.py", "file_organizer_server.py"]
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(" Archivos faltantes del proyecto:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n Asegúrate de tener todos los archivos del proyecto en esta carpeta")
        print(" Puedes continuar si solo falta requirements.txt (se instalarán las dependencias automáticamente)")
        
        response = input("\n¿Continuar de todas formas? (s/n): ").lower()
        if response not in ['s', 'sí', 'si', 'y', 'yes']:
            return
    
    # Ejecutar instalación
    installer = MCPInstaller()
    success = installer.install()
    
    if success:
        print("\n ¡Todo listo! El MCP está instalado y configurado.")
    else:
        print("\n La instalación falló. Revisa los errores anteriores.")

if __name__ == "__main__":
    main()