# 🤖 AnalaiBot - Asistente IA para Analaizer.digital

Este proyecto implementa un asistente conversacional con Inteligencia Artificial diseñado para representar a la academia **Analaizer.digital**. El bot responde preguntas sobre los cursos, contenidos, eventos, precios y otros aspectos de la academia, y es capaz de registrar leads y dudas no resueltas mediante herramientas externas como **Pushover**.

---

## 🚀 Características

- Responde a preguntas usando información de archivos PDF y TXT.
- Registra nuevos usuarios interesados con sus datos personales.
- Guarda preguntas desconocidas para seguir mejorando el contenido.
- Usa herramientas definidas como funciones (`tools`) que el agente puede invocar.
- Comunicación en tiempo real a través de [Gradio](https://www.gradio.app/).
- Notificaciones automáticas mediante [Pushover](https://pushover.net/).

---

## 📦 Requisitos

```bash
python 3.10+
```

## Instalación de dependencias:

```shell
pip install -r requirements.txt
```

```shell
uv add python-dotenv pypdf gradio openai requests
```

## Estructura del Proyecto

.
├── datos-academia/
│   ├── description.pdf       # PDF con la descripción completa de la academia
│   ├── explicacion.txt       # Explicación extensa sobre los contenidos
│   └── summary.txt           # Resumen estructurado
├── .env                      # Variables de entorno (API keys de OpenAI y Pushover)
├── chatbot.py                # Archivo principal que lanza el asistente
└── README.md                 # Este documento

## ⚙️ Configuración

### ✅ Variables de entorno

Crea un archivo `.env` con el siguiente contenido:
PUSHOVER_USER=tu_user_key
PUSHOVER_TOKEN=tu_token_key
OPENAI_API_KEY=tu_api_key_openai

## 📚 Archivos necesarios

Coloca los siguientes archivos en la carpeta datos-academia/:

* description.pdf
* explicacion.txt
* summary.txt

## 🧠 ¿Cómo funciona?
### 🔧 Herramientas integradas (tools)

El bot puede usar estas herramientas cuando detecte que debe registrar información:
record_user_details(email, name, notes): Registra los datos de un posible alumno.
record_unknown_question(question): Guarda preguntas que no pudo responder.
Ambas herramientas usan Pushover para enviar notificaciones al administrador.

### 📜 Contexto personalizado

El bot se inicializa con un system_prompt que incluye información de los archivos y las instrucciones sobre cómo debe comportarse.

### 💬 Interfaz de chat

Se utiliza Gradio para lanzar una interfaz web de chat. Puedes ejecutarla así:

```shell
uv run app.py
```

### 🧪 Ejemplo de uso

```
Usuario: ¿Qué cursos tenéis sobre analítica avanzada?

Bot: En nuestra academia contamos con formaciones especializadas en analítica digital, incluyendo GA4, GTM y BigQuery. ¿Te gustaría que te envíe el detalle completo?

Usuario: Sí, me interesa. Mi correo es ana@example.com

Bot: ¡Perfecto, Ana! He registrado tu correo para que podamos enviarte toda la información personalizada. ¿Hay algún tema que te interese especialmente?
```

## 🛠 Posibles mejoras futuras

* Almacenamiento de leads en una base de datos o CRM.
* Entrenamiento adicional con interacciones reales.
* Integración con sistemas de automatización de email marketing.

## 📬 Contacto

¿Tienes dudas, sugerencias o quieres colaborar?

Escríbeme a: [hola@javilazaro.es](mailto:hola@javilazaro.es)