# main.py
from tkinter import *
from PIL import Image, ImageTk
import urllib.request
import requests
import json
import os

# Importamos a los dos asistentes
from asistente import AsistenteQuizAnimales
from asistente_info import AsistenteInfoAnimales

class FirulaisGuesserApp:
    """Clase principal que maneja la interfaz y lógica del juego y la enciclopedia."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PERROS")
        self.root.geometry("1500x750")
        
        # instanciamos ambos bots
        self.bot_quiz = AsistenteQuizAnimales()
        self.bot_info = AsistenteInfoAnimales()
        
        self.api_url = "https://dog.ceo/api/breeds/image/random"
        self.url_actual_imagen = ""
        self.intentos = 0
        
        # sistema de guardado
        self.archivo_puntaje = "puntaje.json"
        self.puntaje = {"adivinados": 0, "fallados": 0}
        self.cargar_puntaje()
        
        # imagen de fondo
        self.fondo_perros = Image.open("fondo_perros.jpeg")
        self.fondo_perros = self.fondo_perros.resize((1500, 750))
        self.imagen_fondo = ImageTk.PhotoImage(self.fondo_perros)
        
        self.construir_interfaz()

    def cargar_puntaje(self):
        if os.path.exists(self.archivo_puntaje):
            try:
                with open(self.archivo_puntaje, "r") as f:
                    self.puntaje = json.load(f)
            except Exception:
                pass

    def guardar_puntaje(self):
        try:
            with open(self.archivo_puntaje, "w") as f:
                json.dump(self.puntaje, f)
        except Exception as e:
            print(f"Error al guardar puntuación: {e}")

    def actualizar_label_puntaje(self):
        texto = f"🏆 Adivinados: {self.puntaje['adivinados']} | ❌ Fallados: {self.puntaje['fallados']}"
        self.label_puntaje.config(text=texto)

    def obtener_respuesta_api(self, url):
        return requests.get(url, timeout=5)

    def construir_interfaz(self):
        # MENU
        self.frame_menu = Frame(self.root, width=1500, height=750)
        self.frame_menu.pack(fill=BOTH, expand=True)

        bg_menu = Label(self.frame_menu, image=self.imagen_fondo)
        bg_menu.place(x=0, y=0, relwidth=1, relheight=1)
        
        titulo_menu = Label(self.frame_menu, text="FIRULAIS GUESSER", fg="#E1D186", bg="#413315", font=("Terminal", 45), padx=20, pady=10)
        titulo_menu.pack(pady=50)

        descripcion = Label(self.frame_menu, text="Aprende sobre perros o pon a prueba tus conocimientos.", fg="#5C5247", bg="#E8E4B1", font=("Lucida console", 14), pady=10)
        descripcion.pack(pady=30)
        
        boton_jugar = Button(self.frame_menu, text="JUGAR TRIVIA", command=self.iniciar_juego, font=("Lucida console", 16, "bold"), bg="#413315", fg="#E1D186", padx=20, pady=10)
        boton_jugar.pack(pady=10)

        boton_info = Button(self.frame_menu, text="EXPLORADOR DE RAZAS", command=self.iniciar_modo_info, font=("Lucida console", 16, "bold"), bg="#5C5247", fg="#E1D186", padx=20, pady=10)
        boton_info.pack(pady=10)

        boton_salir = Button(self.frame_menu, text="Salir de la App", command=self.root.quit, font=("Lucida console", 12), bg="#413315", fg="#FFFFFF", padx=10, pady=5)
        boton_salir.pack(pady=20)
        
        # PANTALLA DE JUEGO
        self.frame_juego = Frame(self.root, width=1500, height=750)
        
        bg_juego = Label(self.frame_juego, image=self.imagen_fondo)
        bg_juego.place(x=0, y=0, relwidth=1, relheight=1)

        titulo_juego = Label(self.frame_juego, text="Modo Trivia", fg="#ADA26C", bg="#413315", font=("Terminal", 40), pady=10)
        titulo_juego.pack(pady=10)

        self.label_puntaje = Label(self.frame_juego, font=("Lucida console", 14, "bold"), fg="#413315", bg="#E1D186", pady=5, padx=10)
        self.label_puntaje.pack(pady=5)
        self.actualizar_label_puntaje()

        self.panel_juego = Label(self.frame_juego)
        self.panel_juego.pack(pady=15)

        self.caja_input_usuario = Entry(self.frame_juego, font=("Lucida console", 14), width=35)
        self.caja_input_usuario.pack(pady=5)

        frame_botones_juego = Frame(self.frame_juego, bg="#E1D186")
        frame_botones_juego.pack(pady=5)

        self.boton_enviar = Button(frame_botones_juego, text="Adivinar Raza", command=self.enviar_respuesta_a_groq, font=("Lucida console", 11, "bold"), bg="#413315", fg="#E1D186")
        self.boton_enviar.grid(row=0, column=0, padx=5)

        self.boton_pista = Button(frame_botones_juego, text="💡 Pedir Pista", command=self.pedir_pista, font=("Lucida console", 11, "bold"), bg="#5C5247", fg="#E1D186")
        self.boton_pista.grid(row=0, column=1, padx=5)

        self.label_output_groq_juego = Label(self.frame_juego, text="Cargando trivia...", fg="#413315", bg="#E1D186", font=("Lucida console", 11), wraplength=550, justify="center")
        self.label_output_groq_juego.pack(pady=15)

        self.boton_otro_juego = Button(self.frame_juego, text="Ver otro perro", command=self.nueva_foto_juego, font=("Lucida console", 12), bg="#E8E4B1", fg="#5C5247")
        self.boton_otro_juego.pack(pady=5)
        
        boton_regresar_1 = Button(self.frame_juego, text="Volver al Menú", command=self.volver_al_menu, font=("Lucida console", 10), bg="#5C5247", fg="#E1D186")
        boton_regresar_1.pack(pady=5)

        # PANTALLA EXPLORADOR
        self.frame_info = Frame(self.root, width=1500, height=750)
        
        bg_info = Label(self.frame_info, image=self.imagen_fondo)
        bg_info.place(x=0, y=0, relwidth=1, relheight=1)

        titulo_info = Label(self.frame_info, text="Explorador de Razas", fg="#ADA26C", bg="#413315", font=("Terminal", 40), pady=10)
        titulo_info.pack(pady=10)

        self.panel_info = Label(self.frame_info)
        self.panel_info.pack(pady=15)

        # Etiqueta grande para mostrar la enciclopedia (textos largos)
        self.label_output_groq_info = Label(self.frame_info, text="Buscando un firulais para analizar...", fg="#413315", bg="#E1D186", font=("Lucida console", 12), wraplength=800, justify="left", padx=20, pady=20)
        self.label_output_groq_info.pack(pady=15)

        self.boton_otro_info = Button(self.frame_info, text="Descubrir otra raza", command=self.nueva_foto_info, font=("Lucida console", 14, "bold"), bg="#413315", fg="#E1D186")
        self.boton_otro_info.pack(pady=10)

        boton_regresar_2 = Button(self.frame_info, text="Volver al Menú", command=self.volver_al_menu, font=("Lucida console", 10), bg="#5C5247", fg="#E1D186")
        boton_regresar_2.pack(pady=5)

    # --- METODOS DE NAVEGACION ---
    def iniciar_juego(self):
        self.frame_menu.pack_forget()
        self.frame_info.pack_forget()
        self.frame_juego.pack(fill=BOTH, expand=True)
        self.nueva_foto_juego()

    def iniciar_modo_info(self):
        self.frame_menu.pack_forget()
        self.frame_juego.pack_forget()
        self.frame_info.pack(fill=BOTH, expand=True)
        self.nueva_foto_info()

    def volver_al_menu(self):
        self.frame_juego.pack_forget()
        self.frame_info.pack_forget()
        self.frame_menu.pack(fill=BOTH, expand=True)

    # --- METODOS DE LÓGICA: MODO INFO ---
    def nueva_foto_info(self):
        self.label_output_groq_info.config(text="Buscando un perro y analizando su raza... Espera un momento.")
        self.boton_otro_info.config(state=DISABLED)
        self.bot_info.limpiar_historial()
        self.root.update()
        
        try:
            http_request_response = self.obtener_respuesta_api(self.api_url)
            data = http_request_response.json()
            self.url_actual_imagen = data["message"]

            urllib.request.urlretrieve(self.url_actual_imagen, "foto_info.jpg")
            img = Image.open("foto_info.jpg")

            nuevo_tamy = 200
            original_tamx, original_tamy = img.size
            nuevo_tamx = int((nuevo_tamy/original_tamy)*original_tamx)
            img = img.resize((nuevo_tamx, nuevo_tamy))

            tk_img = ImageTk.PhotoImage(img)
            self.panel_info.config(image=tk_img)
            self.panel_info.image = tk_img
            
            # Pedimos la información a la IA pasándole la imagen para que extraiga la raza
            respuesta_enciclopedia = self.bot_info.preguntar(
                mensaje="", 
                url_imagen=self.url_actual_imagen
            )
            self.label_output_groq_info.config(text=respuesta_enciclopedia)
            
        except Exception as e:
            self.label_output_groq_info.config(text=f"Error de conexión: {e}")
        finally:
            self.boton_otro_info.config(state=NORMAL)

    # --- METODOS DE LÓGICA: MODO JUEGO (QUIZ) ---
    def pedir_pista(self):
        self.label_output_groq_juego.config(text="Pensando una pista...")
        self.root.update()
        try:
            respuesta_pista = self.bot_quiz.preguntar("Dame una breve pista o dato curioso para adivinar a este perro, pero bajo ninguna circunstancia digas el nombre de la raza ni la palabra 'CODIGO_VICTORIA'.")
            self.label_output_groq_juego.config(text=f"💡 Pista: {respuesta_pista}\n\n[Intentos restantes: {3 - self.intentos}]")
        except Exception as e:
            self.label_output_groq_juego.config(text=f"Error al conectar con la IA: {e}")

    def nueva_foto_juego(self):
        self.intentos = 0
        self.caja_input_usuario.config(state=NORMAL)
        self.boton_enviar.config(state=NORMAL)
        self.boton_pista.config(state=NORMAL)
        
        self.boton_otro_juego.config(text="Ver otro perro", font=("Lucida console", 12), bg="#E8E4B1", fg="#5C5247")
        self.bot_quiz.raza_correcta = None
        self.bot_quiz.limpiar_historial()
        
        self.label_output_groq_juego.config(text="Buscando un firulais... Espera un momento.")
        self.root.update()
        
        try:
            http_request_response = self.obtener_respuesta_api(self.api_url)
            data = http_request_response.json()
            self.url_actual_imagen = data["message"]

            urllib.request.urlretrieve(self.url_actual_imagen, "foto_juego.jpg")
            img = Image.open("foto_juego.jpg")

            nuevo_tamy = 200
            original_tamx, original_tamy = img.size
            nuevo_tamx = int((nuevo_tamy/original_tamy)*original_tamx)
            img = img.resize((nuevo_tamx, nuevo_tamy))

            tk_img = ImageTk.PhotoImage(img)
            self.panel_juego.config(image=tk_img)
            self.panel_juego.image = tk_img
            
            respuesta_inicial = self.bot_quiz.preguntar(
                mensaje="¡Hola! Comienza el juego de trivia con esta imagen.", 
                url_imagen=self.url_actual_imagen
            )
            self.label_output_groq_juego.config(text=f"{respuesta_inicial}\n\n[Intentos restantes: 3]")
        except Exception as e:
            self.label_output_groq_juego.config(text=f"Error al conectar con el servidor: {e}\nIntenta presionar 'Ver otro perro'.")
        
        self.caja_input_usuario.delete(0, END)

    def enviar_respuesta_a_groq(self):
        respuesta_usuario = self.caja_input_usuario.get()
        
        if not respuesta_usuario.strip():
            return
            
        self.intentos += 1
        intentos_restantes = 3 - self.intentos
            
        try:
            prompt_seguro = (
                f"Mi respuesta es: '{respuesta_usuario}'. "
                "Evalúa si es correcta. IMPORTANTE: Si adiviné la raza exacta,"
                "incluye siempre, sin fallar, todo el tiempo, obligatoriamente la palabra 'CODIGO_VICTORIA' en tu respuesta. "
                "Si me equivoqué, responde normalmente sin usar esa palabra clave."
            )
            respuesta_bot = self.bot_quiz.preguntar(prompt_seguro)
        except Exception as e:
            self.intentos -= 1
            self.label_output_groq_juego.config(text=f"Error de conexión con la IA: {e}\nIntenta adivinar nuevamente.")
            return

        self.caja_input_usuario.delete(0, END)
        
        es_victoria = "CODIGO_VICTORIA" in respuesta_bot
        respuesta_limpia = respuesta_bot.replace("CODIGO_VICTORIA", "").strip()
        
        if es_victoria:
            self.puntaje["adivinados"] += 1
            self.guardar_puntaje()
            self.actualizar_label_puntaje()
            
            self.caja_input_usuario.config(state=DISABLED)
            self.boton_enviar.config(state=DISABLED)
            self.boton_pista.config(state=DISABLED)
            
            self.label_output_groq_juego.config(text=f"¡CORRECTO!\n\n{respuesta_limpia}")
            self.boton_otro_juego.config(text="SIGUIENTE PERRO", font=("Lucida console", 14, "bold"), bg="#90EE90", fg="#000000")
            
        elif self.intentos >= 3:
            self.puntaje["fallados"] += 1
            self.guardar_puntaje()
            self.actualizar_label_puntaje()
            
            self.caja_input_usuario.config(state=DISABLED)
            self.boton_enviar.config(state=DISABLED)
            self.boton_pista.config(state=DISABLED)
            
            correcta = getattr(self.bot_quiz, "raza_correcta", "la raza correcta")
            mensaje_final = f"{respuesta_limpia}\n\n ¡Has agotado todos tus intentos! La respuesta correcta es: {correcta}. Puedes continuar jugando cambiando de perro."
            self.label_output_groq_juego.config(text=mensaje_final)
            self.boton_otro_juego.config(text="VER OTRO PERRO", font=("Lucida console", 16, "bold"), bg="#FFD700", fg="#000000")
            
        else:
            self.label_output_groq_juego.config(text=f"{respuesta_limpia}\n\n[Intentos restantes: {intentos_restantes}]")

if __name__ == "__main__":
    root = Tk()
    app = FirulaisGuesserApp(root)
    root.mainloop()
