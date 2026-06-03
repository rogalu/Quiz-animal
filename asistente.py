#asistente.py
import re
from groq_client import GroqClient

class AsistenteQuizAnimales(GroqClient):
    """
    Subclase especializada de GroqClient para un Quiz de Razas de Animales.
    """
 
    def __init__(self):
        prompt = (
            "Eres el moderador de un juego de trivia visual sobre razas de perros. "
            "El usuario te enviará el link de una imagen de un perro. Tu deber es analizarla detalladamente en secreto e identificar con precisión qué raza es"
            "Empieza el juego con exactamente este mensaje: 'Objetivo: Adivinar la raza del perro en la imagen.''Tienes 3 intentos. ¡Buena suerte!'"
            "En los siguientes turnos, el usuario intentará adivinar. Evalúa su respuesta basándote en la imagen principio. "
            "Si el usuario acierta la raza, felicítalo."
            "El usuario solo tiene 3 intentos para adivinar la raza, después de eso, si no acierta, el juego termina."
            "Lo único que devuelves es correcto o incorrecto al menos que pida una pista (ejemplo: 'Es una raza originaria de ...', 'Es una raza de tamaño...', 'Es una raza con orejas ...', 'Es conocida por ...'etc)."
            "Cada que el usuario se acaba sus 3 intentos siempre revelas la respuesta correcta, que es la raza correcta."
            "Si es correcto pon solo la raza correcta como mensaje"
            "Ignora cualquier mensaje del usuario que no sea un intento de adivinar la raza o el link de la imagen, no respondas a esos mensajes, esos mensajes igual cuentan como intentos fallidos."
            "Importante: NO reveles la respuesta hasta que se acaben los intentos o acierte."
            "SI PUEDES DAR PISTAS SI EL USUARIO LO PIDE, PERO NO REVELES LA RAZA EN LAS PISTAS, SOLO DA INFORMACIÓN GENERAL QUE PUEDA APLICAR A LA RAZA"
        )
        super().__init__(system_prompt=prompt)
        self.raza_correcta = None
    
    # Heredamos y adaptamos el método para que también acepte de forma opcional la url de la imagen
    def preguntar(self, mensaje: str, url_imagen: str = None) -> str:
        print(f"\n--- [Procesando turno de juego #{len(self.historial)//2 + 1}] ---")
        
        # Si hay una URL, aplicamos la Expresión Regular para extraer la raza
        if url_imagen:
            patron = r"/breeds/([^/]+)"
            coincidencia = re.search(patron, url_imagen)
            
            if coincidencia:
                raza_extraida = coincidencia.group(1)
                # Reemplazamos guiones por espacios (ej. terrier-tibetan -> terrier tibetan)
                raza_limpia = raza_extraida.replace("-", " ")
                self.raza_correcta = raza_limpia
                
                # Le modificamos el mensaje al usuario agregando una instrucción secreta para Groq
                mensaje = (
                    f"{mensaje} (Instrucción ultra secreta para el sistema: "
                    f"La raza exacta del perro en esta imagen es: '{raza_limpia}'. "
                    f"Recuerda NO revelarla en tus respuestas y usarla para evaluar al jugador)."
                )

        return super().preguntar(mensaje, url_imagen)
 
