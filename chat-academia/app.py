import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, date

from openai import OpenAI

from pypdf import PdfReader
import gradio as gr 

load_dotenv(override=True)

#Vamos a crear un chatbot para nuestra academia

def push(text:str):
    """
    Envia el mensaje a través de Pushover a nuestros dispositivos móviles
    """
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "user": os.getenv("PUSHOVER_USER"),
            "token": os.getenv("PUSHOVER_TOKEN"),
            "message": text
        }
    )

def record_user_details(email: str, name: str="Nombre no indicado", notes: str="No proporcionadas"):
    """
        Registra los detalles del usuario.
    """
    push(f"Registrando {name} con el email {email} y la información: {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question: str):
    """
        Guardando las preguntas en las que no tenemos información
    """
    push(f"Registrando: {question}")
    return {"recorded": "ok"}

#Vamos a crear la herramienta que va a poder utilizar nuestro agente para poder otorgar la información de nuestra academia

record_user_details_json = {
    "name" : "record_user_details",
    "description" : "Utilizamos esta herramienta para registrar que un usuario está interesado en entrar en nuestra comunidad, además propociona el correo electrónico",
    "parameters": {
        "type": "object",
        "properties" : {
            "email" : {
                "type": "string",
                "desciption": "La dirección de correo electrónico del usuario"
            },
            "name": {
                "type": "string",
                "desciption" : "Nombre del usuario si es que se indica"
            },
            "notes": {
                "type": "string",
                "desciption": "Información adicional que pueda ser interesante sobre la conversaion que haya uqe registrar para un contexto"
            }
        },
        "required" : ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Utiliza esta herramienta siempre que no puedas responder a las preguntas para poder actualizar la información",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "La pregunta que no se supo responder"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

#Le damos a nuestro agente el contexto para nuestras herramientas
tools = [
    {
        "type": "function",
        "function": record_user_details_json
    },
    {
        "type": "function",
        "function": record_unknown_question_json
    }
]

#Ahora vamos a montar nuestro agente vendedor de nuestra academia
class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "AnalaiBot"
        #Leemos los datos del PDF
        reader = PdfReader("datos-academia/description.pdf")
        self.analaizer = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.analaizer += text
        with open("datos-academia/explicacion.txt", "r", encoding='utf-8') as f:
            self.explicacion = f.read()
        with open("datos-academia/summary.txt", "r", encoding='utf-8') as g:
            self.summary = g.read()

    
    def handle_tool_call(slef, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"La herramienta ha llamado a: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id 
                }
            )
        return results

    def system_prompt(self):
        system_prompt = f"""
            Actúas como {self.name}, el asistente oficial de Analaizer.digital.
            Tu función es responder preguntas en el sitio web de Analaizer.digital, en particular sobre los cursos, masterclasses, profesores, precios, eventos y trayectoria de la academia.
            Dispones de un conjunto de documentos que puedes usar para responder:
            - Un PDF con la descripción completa de la academia.
            - Un archivo de texto con la explicación detallada de los contenidos.
            - Un archivo de texto con un resumen estructurado.

            Tu responsabilidad es representar a Analaizer.digital en las interacciones con los usuarios con la mayor fidelidad posible.
            Debes mostrar un tono cercano, profesional y atractivo, como si hablaras con un potencial alumno interesado en unirse a la academia.

            Si el usuario proporciona información personal como su correo electrónico, nombre, nivel de conocimiento, expectativas de aprendizaje o intereses (por ejemplo, SEO, analítica, automatización, IA), debes registrarlo con la herramienta 'record_user_details'.
            Usa el campo 'notes' para añadir cualquier información extra relevante de la conversación (temas de interés, nivel, expectativas, etc.).

            Si no sabes la respuesta a alguna pregunta, usa la herramienta 'record_unknown_question' para registrar la pregunta que no pudiste responder, incluso si se trata de algo trivial o no relacionado directamente con la academia.

            Tu objetivo final es resolver dudas, aportar información clara sobre los cursos y animar a los usuarios a formar parte de la comunidad de Analaizer.digital.
            """
        
        system_prompt += f"\n\n## Resumen:\n{self.explicacion} y {self.analaizer} \n\n## Perfil de Analaizer: \n{self.analaizer}\n\n"
        system_prompt += f"En este contexto, por favor chatea con el usuario, manteniéndote siempre en el personaje de {self.name}."

        return system_prompt

    def chat(self, message, history):
        """Herramienta para poder chatear con nuestro agente IA

        Args:
            message (_type_): _description_
            history (_type_): _description_
        """
        messages = [
            {
                "role": "system",
                "content": self.system_prompt()
            }
        ] + history + [
            {
                "role": "user",
                "content": message
            }
        ]

        done = False

        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()