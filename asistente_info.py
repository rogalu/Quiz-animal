# asistente_info.py
import re
from groq_client import GroqClient

class AsistenteInfoAnimales(GroqClient):
    """
    Subclase especializada de GroqClient para proporcionar información
    enciclopédica sobre razas de perros.
    """
 
    def __init__(self):
        prompt = (
            "Eres un experto en perros muy amigable y conocedor. "
            "Tu objetivo es proporcionar información estructurada, interesante y resumida"
            "sobre la raza de perro que el usuario te indique si o si."
            "Incluye unicamente en formato de lista los aspectos: -Raza -Origen -Temperamento -Dato Curioso."
            "Cada aspecto es especifico de la raza, no generalices con información que pueda aplicar a muchas razas, se específico con cada raza."
            "Mantén la respuesta en un formato fácil de leer y muy corto con un maximo de 20 palabras."
            "No respondas ninguna otra cosa que no sea la información solicitada sobre la raza de perro."
            "siempre manten el mismo formato"
        )
        super().__init__(system_prompt=prompt)
    
    def preguntar(self, mensaje: str, url_imagen: str = None) -> str:
        # Extraemos la raza de la URL de la misma forma
        if url_imagen:
            patron = r"/breeds/([^/]+)"
            coincidencia = re.search(patron, url_imagen)
            
            if coincidencia:
                raza_extraida = coincidencia.group(1)
                raza_limpia = raza_extraida.replace("-", " ")
                
                # En lugar de un mensaje secreto de juego, le damos la orden directa de informar
                mensaje = f"Ignora el mensaje anterior si lo hay. Háblame sobre la raza de perro '{raza_limpia}' basándote en la imagen proporcionada."

        return super().preguntar(mensaje, url_imagen)