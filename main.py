from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

# Importaciones para la IA de GitHub
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Esto asegura que Python encuentre el .env sin importar desde dónde inicies el servidor
base_dir = os.path.dirname(__file__)
env_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=env_path)

#Iniciamos la app
app = FastAPI()

#Guardamos el token de nuestro github key
token_github = os.getenv("GITHUB_TOKEN")

# Verificamos si el token existe antes de intentar conectarnos
if not token_github:
    print("⚠️ ADVERTENCIA: No se encontró GITHUB_TOKEN en el archivo .env")
    client_ia = None # Lo dejamos nulo para que no rompa el programa al arrancar
else:
    client_ia = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(token_github)
    )


# ---> RUTA A: La de Supabase (Personajes)
@app.get("/api/personajes")
def obtener_personajes():
    url_supabase = f"{os.getenv('SUPABASE_URL')}/rest/v1/PERSONAJE"
    mi_llave = os.getenv("SUPABASE_KEY")
    
    cabeceras = {
        "apikey": mi_llave,
        "Authorization": f"Bearer {mi_llave}"
    }
    
    respuesta = requests.get(url_supabase, headers=cabeceras)
    return respuesta.json()

# ---> RUTA B: La nueva de Inteligencia Artificial
@app.get("/api/ia/preguntar")
def preguntar_ia(pregunta: str):
    # Si el token falló arriba, avisamos al usuario aquí
    if not client_ia:
        return {"error": "El cliente de IA no está configurado. Revisa tu GITHUB_TOKEN en el archivo .env"}
    
    try:
        response = client_ia.complete(
            messages=[
                {"role": "system", "content": "Eres un asistente experto en ingeniería y tecnología."},
                {"role": "user", "content": pregunta},
            ],
            model="gpt-4o-mini"
        )
        return {"respuesta": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}