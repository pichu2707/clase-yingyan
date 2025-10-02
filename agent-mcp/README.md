# 💬 MCP Chat Client - Asistente Conversacional para Organizar Descargas

Este proyecto es un cliente tipo **chat interactivo** para el sistema **MCP (Model Context Protocol)**. Permite ejecutar comandos sobre tu carpeta de descargas mediante lenguaje natural, ideal para demostraciones en clase o para usuarios que prefieren una experiencia conversacional.

---

## 🚀 ¿Qué puedes hacer con este asistente?

- Analizar el contenido de tu carpeta de descargas.
- Organizar archivos por categorías (documentos, imágenes, etc.).
- Crear estructuras de carpetas automáticamente.
- Obtener información específica sobre archivos.
- Limpiar carpetas vacías.
- Todo esto desde una interfaz tipo chat.

---

## 📦 Requisitos

```bash
Python 3.10 o superior
Instala las dependencias necesarias (usa uv si lo tienes disponible):
```

```bash
Copiar código
uv pip install -r requirements.txt
O usando pip:
```

```bash
Copiar código
pip install asyncio pydantic
Asegúrate también de tener los módulos locales file_organizer_server.py y config.py en las rutas ../downloads-mcp/ y ../github-mcp/ respectivamente.
```

### 📁 Estructura del Proyecto

```bash
.
├── mcp_chat_client.py           # Este script
├── ../downloads-mcp/
│   └── file_organizer_server.py # Lógica principal del MCP
├── ../github-mcp/
│   └── config.py                # Configuración de carpetas y categorías
└── README.md
```

## ⚙️ Configuración

Edita el archivo config.py con la ruta correcta a tu carpeta de descargas:

```python
DOWNLOADS_FOLDER = Path("/ruta/a/tu/carpeta/Descargas")
```

También puedes ajustar las categorías de organización en FILE_ORGANIZATION.

## 🧠 ¿Cómo funciona?

El sistema interpreta comandos escritos en lenguaje natural y los asocia con funciones predefinidas como:
* analizar, ver, mostrar: Analiza los archivos de descargas.
* organizar, ordenar: Organiza archivos según categorías.
* estructura, folders: Crea la estructura de carpetas.
* info archivo.pdf: Muestra detalles de un archivo.
* limpiar vacias: Elimina carpetas vacías.
* ayuda: Muestra los comandos disponibles.

## 💬 Ejemplo de Uso

```text

[TU] > analizar completo
[CLAUDE] [12:34:56] Aquí tienes el análisis de tu carpeta:
...

[TU] > organizar documentos en simulación
[CLAUDE] [12:35:10] Iniciando simulación de archivos...

[TU] > info contrato_2023.pdf
[CLAUDE] [12:35:45] Información del archivo:
- Nombre: contrato_2023.pdf
- Tamaño: 1.2MB
...
```

## 🔧 Comandos Disponibles

```text
• analizar               → Ver archivos y su clasificación
• organizar             → Organizar archivos (simulación o real)
• estructura            → Crear estructura de carpetas
• info archivo.pdf      → Ver información de un archivo
• limpiar vacias        → Borrar carpetas vacías
• ayuda                 → Ver todos los comandos
• salir                 → Terminar el chat
```

Puedes usar variaciones como:

```text
• organizar real
• organizar imágenes
• analizar completo
• info setup.exe
```

## ▶️ Ejecutar el chat

```bash
python mcp_chat_client.py
```

Esto iniciará el asistente con mensajes tipo chat y sugerencias contextuales.

## 🧪 Ideal para...

* Talleres educativos sobre automatización.
* Usuarios no técnicos que quieren organizar archivos fácilmente.
* Demostraciones de agentes MCP conversacionales.

## 📬 Contacto

¿Tienes dudas, quieres mejorar el sistema o colaborar?
Escríbeme a: [hola@javilazaro.es](mailto:hola@javilazaro.es)