#groq_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    """
    Cliente base para interactuar con la API de Groq.
    Encapsula la configuración de conexión y el historial de conversación.
    """

    def __init__(self, system_prompt: str = "Eres un asistente útil."):
        self.__api_key = os.getenv("GROQ_API_KEY")
       
        if not self.__api_key:
            raise ValueError("Error: La variable de entorno 'GROQ_API_KEY' no está configurada")

        self.__cliente = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=self.__api_key)
        self.__system_prompt = system_prompt
        self.historial = []
        self.modelo = "meta-llama/llama-4-scout-17b-16e-instruct"
 
    def _construir_mensajes(self) -> list:
        mensajes = [{"role": "system", "content": self.__system_prompt}]
        mensajes.extend(self.historial)
        return mensajes
 
    def preguntar(self, mensaje: str, url_imagen: str = None) -> str:
        # Si nos pasan una URL de imagen, construimos el formato multimodal (Texto + Imagen)
        if url_imagen:
            contenido_mensaje = [
                {"type": "text", "text": mensaje},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url_imagen
                    }
                }
            ]
        else:
            contenido_mensaje = mensaje        
        
        # Se guarda 'contenido_mensaje' en el historial para incluir la imagen en la API
        self.historial.append({"role": "user", "content": contenido_mensaje})

        respuesta = self.__cliente.chat.completions.create(
            model=self.modelo,
            messages=self._construir_mensajes()
        )

        texto_respuesta = respuesta.choices[0].message.content
        self.historial.append({"role": "assistant", "content": texto_respuesta})

        return texto_respuesta
 
    def limpiar_historial(self):
        self.historial = []
 
    def __str__(self):
        return f"GroqClient | modelo: {self.modelo} | mensajes en historial: {len(self.historial)}"
