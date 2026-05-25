from groq_client import GroqClient

class AsistenteQuizAnimales(GroqClient):
    """
    Subclase especializada de GroqClient para un Quiz de Razas de Animales.
    """
 
    def __init__(self):
        prompt = (
            "Eres un experto experto en zoología y razas de animales (perros, gatos, caballos, aves, etc.). "
            "Tu objetivo es actuar estrictamente como un juego de quiz o trivia interactiva. "
            "Debes proponer preguntas desafiantes al usuario sobre características físicas, orígenes, temperamentos o datos curiosos de diferentes razas. "
            "Plantea una pregunta a la vez y espera a que el usuario responda antes de evaluarlo. "
            "Sé muy dinámico, entusiasta y valida las respuestas con amabilidad, explicando brevemente el porqué si el usuario falla."
        )
        super().__init__(system_prompt=prompt)
 
    def preguntar(self, mensaje: str) -> str:
        # Llama a la función original del padre para obtener la respuesta de la IA
        print(f"\n--- [Procesando turno de juego #{len(self.historial)//2 + 1}] ---")
        return super().preguntar(mensaje)
 
    def modo_rapido(self, pregunta: str) -> str:
        # Modifica la consulta para forzar respuestas directas y breves en la trivia.
        consulta_breve = f"{pregunta} (Responde o formula tu pregunta en máximo 2 oraciones)."
        return self.preguntar(consulta_breve)