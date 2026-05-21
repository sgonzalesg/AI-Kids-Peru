# Liberías estándar
import os
import json
import requests
from PIL import Image
from io import BytesIO

# Librerías de Google AI Studio
from google import genai
from google.genai import types

# Variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Configuración: API Key de Google AI Studio
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Inicializamos el cliente
client = genai.Client(api_key=GOOGLE_API_KEY)

def auditar_evidencia_cientifica(descripcion_alumno, url_imagen):
    print("[Agente Maestro] Conectando con Gemini.")

    # SOUL.md: La identidad del agente
    with open("config/SOUL.md", "r", encoding="utf-8") as f:
        soul_prompt = f.read().strip()

    # INSTINCT.md: Las reglas de validación estricta
    with open("config/INSTINCT.md", "r", encoding="utf-8") as f:
        instinct_template = f.read().replace("{descripcion_alumno}", descripcion_alumno).strip()
        instinct_prompt = instinct_template

    try:
        # Descargamos la imagen en memoria
        print("Descargando evidencia.")
        respuesta_img = requests.get(url_imagen)
        img = Image.open(BytesIO(respuesta_img.content))

        # Lanzamos el análisis con Gemini 3.5 Flash
        print("Evaluando parámetros científicos.")
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[instinct_prompt, img],
            config=types.GenerateContentConfig(
                system_instruction=soul_prompt,
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "aprobado": {"type": "BOOLEAN"},
                        "motivo": {"type": "STRING"}
                    },
                    "required": ["aprobado", "motivo"]
                }
            )
        )
        
        # Procesamos la respuesta de Gemini
        resultado_texto = response.text.strip()
        print(f"[Respuesta de Gemini]: {resultado_texto}")
        return json.loads(resultado_texto)

    except Exception as e:
        print(f"Fallo crítico en el Agente: {str(e)}")
        return {"aprobado": False, "motivo": "Error conectando con Google."}

# Bloque de prueba
if __name__ == "__main__":
    foto_prueba = "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcR-RQH2HLAQQQ87Mn1xkARn7Jm3figf2iL-pc24-J_mVQpqd6eyM7Kla94D5F1ZWbvLBDXh0tqQ__veR1E7aFTD8DWu&s=19"
    desc_prueba = "Muestra del Río Rímac"
    
    resultado = auditar_evidencia_cientifica(desc_prueba, foto_prueba)
    print("\nVeredicto Final:", resultado)