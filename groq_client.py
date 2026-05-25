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
        # Carga la API key y la guarda en un atributo privado __api_key
        self.__api_key = os.getenv("GROQ_API_KEY")
       
        # Si no existe la variable de entorno, lanza un ValueError
        if not self.__api_key:
            raise ValueError("Error: La variable de entorno 'GROQ_API_KEY' no está configurada")

        # Crea el cliente de OpenAI apuntando a la base_url de Groq
        self.__cliente = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=self.__api_key)

        # Guarda el system_prompt en un atributo privado __system_prompt
        self.__system_prompt = system_prompt

        # Inicializa el historial como una lista vacía
        self.historial = []

        # Modelo a usar
        self.modelo = "llama-3.3-70b-versatile"
 
 
    def _construir_mensajes(self) -> list:
        # El primer elemento siempre es el system prompt
        mensajes = [{"role": "system", "content": self.__system_prompt}]

        # Agrega todos los mensajes del historial
        mensajes.extend(self.historial)

        return mensajes
 
 
    def preguntar(self, mensaje: str) -> str:
        # 1. Agrega el mensaje del usuario al historial
        self.historial.append({"role": "user", "content": mensaje})

        # 2. Llama a la API de Groq
        respuesta = self.__cliente.chat.completions.create(
            model=self.modelo,
            messages=self._construir_mensajes()
        )

        # 3. Extrae el texto de la respuesta
        texto_respuesta = respuesta.choices[0].message.content

        # 4. Agrega la respuesta de la IA al historial para mantener el contexto
        self.historial.append({"role": "assistant", "content": texto_respuesta})

        # 5. Retorna el resultado
        return texto_respuesta
 
 
    def limpiar_historial(self):
        self.historial = []
 
 
    def __str__(self):
        return f"GroqClient | modelo: {self.modelo} | mensajes en historial: {len(self.historial)}"