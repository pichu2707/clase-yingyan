# Charla de Agentes IA, MCP para la academia de Ying Yang SEO

# Documento de Diseño

## Resumen

El diseño se enfoca en corregir los errores identificados en el sistema de notificaciones y en mejorar la robustez del manejo de errores. Los principales problemas son errores tipográficos en nombres de variables y funciones, y la falta de manejo de errores en el sistema de notificaciones.

## Arquitectura

El sistema mantiene su arquitectura actual con las siguientes mejoras:

```markdown
ChatBot (Clase Me)
├── Integración con OpenAI
├── Sistema de Manejo de Herramientas
│ ├── record_user_details (corregido)
│ └── record_unknown_question (corregido)
└── Sistema de Notificaciones (Pushover)
├── Configuración del Entorno
├── Manejo de Errores
└── Registro de Logs
```


## Componentes e Interfaces

### 1. Sistema de Notificaciones (función `push`)

**Problemas actuales:**
- Error tipográfico en el nombre de la variable de entorno: `PUHSOVER_TOKEN` → `PUSHOVER_TOKEN`
- Sin manejo de errores para solicitudes fallidas
- Sin validación de las variables de entorno

**Diseño mejorado:**
```python
def push(text: str) -> bool:
    """
    Envía una notificación mediante Pushover con manejo de errores
    Retorna True si fue exitoso, False en caso contrario
    """
    # Validar las variables de entorno
    # Enviar la solicitud con manejo de errores
    # Registrar los errores adecuadamente
    # Retornar el estado de éxito

### 2. Funciones de Herramientas

def record_user_details(email: str, name: str="Nombre no indicado", notes: str="No proporcionadas") -> dict:
    """Mejorado con validación y manejo de errores"""

def record_unknown_question(question: str) -> dict: 
    """Mejorado con validación y manejo de errores"""
```

### 3. Registro de Herramientas

### Problemas actuales:

1. No hay validación de los resultados de ejecución de herramientas

2. Diseño mejorado:

- Mapeo correcto del nombre de la función
- Nombres consistentes entre definiciones de funciones y esquemas JSON
- Manejo de errores mejorado en handle_tool_call
- Modelos de Datos
- Configuración del Entorno

```python
REQUIRED_ENV_VARS = {
    "PUSHOVER_USER": "Clave de usuario de Pushover",
    "PUSHOVER_TOKEN": "Token de aplicación de Pushover" 
}
```

## Formato de respuesta de herramietnas

```python
{
    "recorded": "ok",
    "notification_sent": bool,
    "error": str | None
}
```

## Manejo de Errores

1. Validación de Variables de Entorno

- [] Comprobar credenciales necesarias de Pushover al iniciar
- [] Proporcionar mensajes de error claros si falta alguna configuración
- [] Permitir una degradación controlada si las notificaciones no están disponibles

2. Manejo de Errores de Red

- [] Capturar y registrar errores de la API de Pushover
- [] Implementar lógica de reintentos para fallos transitorios
- [] Continuar con la funcionalidad del chat incluso si fallan las notificaciones

3. Manejo de Errores en Ejecución de Herramientas

- [] Validar los argumentos de las herramientas antes de ejecutar
- [] Manejar excepciones en las funciones de herramientas
- [] Retornar respuestas de error significativas al LLM
- [] Estrategia de Pruebas

1. Pruebas Unitarias

- [x] Probar la función push con credenciales válidas e inválidas
- [] Probar funciones de herramientas con varios escenarios de entrada
- [] Probar rutas de manejo de errores

2. Pruebas de Integración

- [x] Probar el flujo completo desde la llamada a la herramienta por el LLM hasta la notificación
- [] Probar escenarios de error (fallos de red, credenciales inválidas)
- [] Verificar que el chat continúe funcionando cuando las notificaciones fallan

3. Pruebas Manuales

- [x] Verificar que las notificaciones aparezcan en dispositivos móviles
- [x] Probar con interacciones reales de usuarios
- [] Validar que los mensajes de error sean útiles
- [] Enfoque de Implementación

* Fase 1: Corregir Errores Críticos

- [x] Corregir el error tipográfico en la variable de entorno PUSHOVER_TOKEN
- [x] Corregir el nombre de la función de record_unknow_question a record_unknown_question
- [x] Actualizar el esquema JSON para que coincida con el nombre corregido

* Fase 2: Añadir Manejo de Errores

- [] Mejorar la función push con validación y manejo de errores
- [] Añadir manejo de errores a las funciones de herramientas
- [] Mejorar el manejo de errores del método handle_tool_call