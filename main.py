from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv #liberia para hacer

# 1. Le decimos a Python que lea el archivo .env y cargue los secretos
load_dotenv()

app = FastAPI()

# Creacion de ruta
@app.get("/api/personaje")
def obtener_personajes():
    
    #Variable que guarda el url de supabase hacia la tabla PERSONAJES
    url_supabase = "https://izlcprswslrsmunpklny.supabase.co/rest/v1/PERSONAJE"
    
    #Contraseña desde el archivo env
    mi_llave = os.getenv("SUPA_BASE_KEY")
    
    # Diccionario con las cabeceras
    cabeceras = {
        "apikey": mi_llave,
    }
    
    #Hacemos la llamada GET a Supabase
    respuesta = requests.get(url_supabase, headers=cabeceras)
    
    # Devuelve el json
    return respuesta.json()