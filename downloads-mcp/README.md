# 🗂️ Organizador de Archivos MCP

Un servidor MCP (Model Context Protocol) básico en Python para organizar automáticamente los archivos de la carpeta de descargas de Windows.

## 🎯 ¿Qué hace este proyecto?

Este MCP proporciona herramientas para:
- **Analizar** archivos en la carpeta de descargas
- **Organizar** archivos por categorías (Documentos, Imágenes, Videos, etc.)
- **Crear** estructura de carpetas organizadas
- **Limpiar** carpetas vacías
- **Obtener información** detallada de archivos específicos

## 🛠️ Instalación

### Instalación con UV (Recomendada - Más rápida)

UV es un gestor de paquetes de Python ultrarrápido. Si ya lo tienes instalado:

#### Opción 1: Script automático
```bash
# Windows
setup_uv.bat

# Linux/Mac  
chmod +x setup_uv.sh
./setup_uv.sh
```

#### Opción 2: Comandos manuales
```bash
# Inicializar proyecto
uv init --name file-organizer-mcp --no-readme

# Añadir dependencias
uv add mcp pydantic

# Verificar
uv run python -c "import mcp; print('✅ Listo')"
```

### Instalación con pip/venv (Tradicional)

Si no tienes UV instalado:

### 1. Clonar/Descargar el proyecto
```bash
# Crear carpeta del proyecto
mkdir file_organizer_mcp
cd file_organizer_mcp

# Copiar los archivos del proyecto aquí
```

### 2. Crear entorno virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Con UV (Recomendado)

```bash
# Demostración completa
uv run python demo.py

# Pruebas básicas  
uv run python test_client.py

# Ejecutar servidor MCP
uv run python file_organizer_server.py

# Gestión de dependencias
uv add [nueva-dependencia]    # Añadir paquete
uv remove [dependencia]       # Quitar paquete
uv sync                       # Sincronizar entorno
uv lock                       # Actualizar lockfile
```

### Con Claude (Cualquier método)

1. **Ejecutar el servidor MCP:**
```bash
# Con UV
uv run python file_organizer_server.py

# Con venv tradicional
python file_organizer_server.py
```

2. **Configurar en Claude:**
   - El servidor se ejecuta en modo stdio
   - Claude puede conectarse directamente al servidor
   - Usar las herramientas disponibles a través de la interfaz de Claude

### Modo tradicional (venv)

1. **Ejecutar pruebas:**
```bash
python test_client.py
```

2. **Verificar configuración:**
   - El script probará los imports
   - Mostrará la categorización de archivos
   - Verificará la carpeta de descargas

## 🔧 Herramientas disponibles

### 1. `analyze_downloads`
**Descripción:** Analiza los archivos en la carpeta de descargas
```json
{
  "name": "analyze_downloads",
  "arguments": {
    "show_details": true
  }
}
```

**Salida:**
- Número total de archivos
- Distribución por categorías
- Tamaño total ocupado
- Detalles de archivos más grandes (opcional)

### 2. `organize_files`
**Descripción:** Organiza archivos en carpetas por categoría
```json
{
  "name": "organize_files",
  "arguments": {
    "dry_run": true,
    "categories": ["Documentos", "Imágenes"]
  }
}
```

**Parámetros:**
- `dry_run`: Si es `true`, solo simula (no mueve archivos)
- `categories`: Lista de categorías específicas a organizar (opcional)

### 3. `create_folder_structure`
**Descripción:** Crea la estructura de carpetas para organización
```json
{
  "name": "create_folder_structure",
  "arguments": {
    "base_folder": "C:/Users/Usuario/Downloads"
  }
}
```

### 4. `get_file_info`
**Descripción:** Información detallada de un archivo específico
```json
{
  "name": "get_file_info",
  "arguments": {
    "filename": "documento.pdf"
  }
}
```

### 5. `cleanup_empty_folders`
**Descripción:** Elimina carpetas vacías de la estructura organizada
```json
{
  "name": "cleanup_empty_folders",
  "arguments": {
    "dry_run": true
  }
}
```

## 📁 Estructura de organización

Los archivos se organizan en las siguientes categorías:

| Categoría | Extensiones |
|-----------|-------------|
| **Documentos** | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt` |
| **Imágenes** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp` |
| **Videos** | `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm` |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma` |
| **Programación** | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.sql` |
| **Comprimidos** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz` |
| **Ejecutables** | `.exe`, `.msi`, `.dmg`, `.deb`, `.rpm` |
| **Hojas de cálculo** | `.xlsx`, `.xls`, `.csv`, `.ods` |
| **Otros** | Cualquier otro tipo de archivo |

## ⚙️ Configuración

### Personalizar categorías
Edita el archivo `config.py` para:
- Agregar nuevas categorías
- Modificar extensiones de archivo
- Cambiar la carpeta de descargas por defecto
- Configurar opciones adicionales

### Opciones disponibles en `config.py`:
```python
SETTINGS = {
    "create_date_folders": True,   # Crear subcarpetas por fecha
    "backup_before_move": False,   # Crear backup antes de mover
    "dry_run": False,              # Modo simulación por defecto
    "log_operations": True,        # Registrar operaciones
}
```

## 🏗️ Estructura del proyecto

```
file_organizer_mcp/
├── venv/                      # Entorno virtual
├── file_organizer_server.py   # Servidor MCP principal
├── config.py                  # Configuración y reglas
├── test_client.py            # Cliente de prueba
├── requirements.txt          # Dependencias
└── README.md                 # Esta documentación
```

## 🎓 Para la clase - Conceptos explicados

### ¿Por qué UV vs pip?

**UV** es un gestor de paquetes moderno que ofrece:
- **🚀 Velocidad**: ~10-100x más rápido que pip
- **🔒 Determinismo**: Lockfiles garantizan reproducibilidad  
- **🛠️ Simplicidad**: Un solo comando para todo
- **🎯 Estándares**: Compatible con pyproject.toml
- **🔄 Resolución**: Mejor resolución de dependencias

**Comparación práctica:**
```bash
# Con pip (tradicional)
python -m venv venv
venv\Scripts\activate  
pip install mcp pydantic
pip freeze > requirements.txt

# Con UV (moderno)
uv add mcp pydantic
# ¡Eso es todo! UV maneja el resto automáticamente
```

### ¿Qué es MCP?
**Model Context Protocol (MCP)** es un protocolo que permite a los modelos de IA (como Claude) interactuar con herramientas externas y sistemas. Piensa en él como un "puente" que permite a la IA:
- Leer archivos de tu computadora
- Ejecutar programas
- Acceder a bases de datos
- Interactuar con APIs

### Componentes del MCP:

1. **Servidor MCP** (`file_organizer_server.py`):
   - Define las herramientas disponibles
   - Implementa la lógica de cada herramienta
   - Maneja las comunicaciones con el cliente

2. **Cliente MCP** (Claude en nuestro caso):
   - Conecta con el servidor
   - Llama a las herramientas según las necesidades
   - Procesa las respuestas

3. **Herramientas (Tools)**:
   - Funciones específicas que puede ejecutar el servidor
   - Cada herramienta tiene parámetros de entrada y salida definidos

### Flujo de trabajo:
```
Claude/Usuario → Solicitud → Servidor MCP → Ejecuta herramienta → Retorna resultado → Claude/Usuario
```

## 🚨 Consideraciones de seguridad

- ⚠️ **Siempre usa `dry_run: true` primero** para simular antes de mover archivos
- 🔒 **Revisa las carpetas de destino** antes de ejecutar
- 💾 **Haz backup** de archivos importantes antes de organizar
- 🧪 **Prueba con pocos archivos** primero

## 🐛 Resolución de problemas

### Error: "Carpeta de descargas no existe"
- Verifica la ruta en `config.py`
- Asegúrate de que tienes permisos de acceso

### Error: "No se pueden importar las dependencias"
- Activa el entorno virtual: `venv\Scripts\activate`
- Instala dependencias: `pip install -r requirements.txt`

### Error: "Archivo en uso"
- Cierra programas que puedan estar usando los archivos
- Ejecuta como administrador si es necesario

## 📚 Próximos pasos

1. **Expandir categorías**: Agregar más tipos de archivo
2. **Reglas avanzadas**: Organizar por fecha, tamaño, etc.
3. **Interfaz gráfica**: Crear una GUI para el organizador
4. **Integración con cloud**: Sincronizar con Google Drive, Dropbox
5. **Machine Learning**: Clasificación inteligente de archivos

## 🤝 Contribuir

Para agregar nuevas funcionalidades:
1. Modifica `config.py` para nuevas reglas
2. Agrega herramientas en `file_organizer_server.py`
3. Actualiza la documentación
4. Prueba con `test_client.py`

---

### Crea estructuras de carpetas
````shell
uv run python -c "
import asyncio
from file_organizer_server import create_folder_structure
from config import DOWNLOADS_FOLDER
async def main():
    result = await create_folder_structure(str(DOWNLOADS_FOLDER))
    for content in result:
        print(content.text)
asyncio.run(main())
"
```

### Sumulación no mueve los archivos

```shell
uv run python -c "
import asyncio
from file_organizer_server import organize_files
async def main():
    result = await organize_files(dry_run=True, categories=None)
    for content in result:
        print(content.text)
asyncio.run(main())
"
```


## Comandos que entenderá (en lenguaje natural):

* **"analiza mi carpeta"** → Análisis completo
* **"organizar simular"** → Ver qué pasaría SIN mover archivos
* **"organizar real"** → MOVER archivos realmente
* **"crear estructura"** → Crear carpetas organizadas
* **"info Django.rar"** → Detalles de archivo específico
* **"organizar solo documentos"** → Solo una categoría
* **"limpiar carpetas vacías"** → Cleanup
* **"ayuda"** → Ver todos los comandos

Para más información puedes contactar conmigo en [hola@javilazaro.es](mailto:hola@javilazaro.es)