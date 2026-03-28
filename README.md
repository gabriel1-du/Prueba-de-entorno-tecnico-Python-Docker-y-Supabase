# Guía de Entornos Virtuales, Docker y Supabase con FastAPI

En este repositorio se encuentra un proyecto que configura un entorno virtual y un contenedor para ejecutar una API conectada a una base de datos en Supabase. El objetivo de esta guía es mostrar, con fines de aprendizaje, los pasos para introducirse en el trabajo con entornos de desarrollo aislados y despliegue de aplicaciones.

## Requisitos previos
Antes de iniciar, es indispensable que tengas instalado y tener conocimientos básicos en:
* Visual Studio Code
* Postman
* Python
* Docker Desktop
* El navegador web de tu preferencia

---

## 1. Creación de la carpeta del proyecto e iniciar entorno

En tu escritorio (o en la ubicación de tu sistema que prefieras), crea una nueva carpeta. Luego, abre esa carpeta usando Visual Studio Code.

Dentro de Visual Studio Code, abre una nueva terminal (en este caso utilizaremos PowerShell) y escribe el siguiente comando:

powershell
python -m venv venv
Nota: Asegúrate de no poner un punto antes de la palabra python.

¿Para qué sirve esto? Este comando creará un entorno virtual dedicado exclusivamente a nuestro proyecto. Esto nos sirve para tener un espacio de trabajo independiente y aislado, en el cual podremos descargar librerías y dependencias sin que se mezclen ni afecten la configuración general de nuestro sistema operativo.

Para ingresar y activar este espacio aislado, escribe el siguiente comando en tu terminal:

PowerShell
.\venv\Scripts\activate
Luego de ejecutarlo, si has seguido correctamente los pasos, verás que al inicio de la línea de tu terminal aparece la palabra (venv). Esto confirma que tu entorno virtual está activo y listo para usarse.

<img width="665" height="65" alt="Foto1" src="https://github.com/user-attachments/assets/3dde5519-4df4-4e45-8814-79795bd5cba4" />

2. Instalación de librerías
Una vez que estamos "adentro" de nuestro entorno virtual activo (revisa que tengas el (venv) en tu terminal), lo que haremos será instalar las herramientas principales que darán vida a nuestro proyecto. En este caso, usaremos dos librerías especializadas para crear APIs que puedan recibir peticiones a través de URLs (rutas web) y ejecutar métodos CRUD (Crear, Leer, Actualizar, Borrar).

En la terminal, escribiremos el siguiente comando:

PowerShell
pip install fastapi uvicorn
¿Qué hace cada una?

FastAPI: Es el marco de trabajo (framework) que nos permite escribir el código de nuestras rutas web de forma rápida y moderna.

Uvicorn: Es el "motor" o servidor web que escuchará las peticiones de los usuarios en internet y las conectará con el código de FastAPI.
<img width="735" height="254" alt="Foto2" src="https://github.com/user-attachments/assets/de7e46b8-e4c0-4970-b2d0-d85e5974756b" />

Una vez que el proceso termine, aparecerán varios mensajes en la terminal confirmando que las librerías se han instalado. Es posible que también te ofrezca un mensaje recomendando actualizar pip (el instalador de Python), lo cual es completamente opcional.

Para verificar que las librerías se instalaron correctamente dentro de nuestra "burbuja" y no afuera, puedes escribir el siguiente comando:

PowerShell
pip list
Este comando imprimirá una lista exacta de todas las librerías que viven actualmente dentro de tu entorno (venv). Deberías ver a fastapi y uvicorn en esa lista junto con sus versiones.

<img width="629" height="312" alt="Foto4" src="https://github.com/user-attachments/assets/658b7d8c-4d96-4402-ad7b-d70d5295da13" />

3. Creación de requirements.txt y Dockerfile
Ahora necesitamos una forma de registrar qué librerías estamos usando. Si el día de mañana un compañero de equipo necesita trabajar en este proyecto, o si queremos subirlo a un servidor, ese otro computador necesita saber exactamente qué instalar.
Para eso usaremos el archivo requirements.txt.

Para crearlo, ejecuta el siguiente comando en la terminal:

PowerShell
pip freeze > requirements.txt
Al ejecutarlo, notarás que en tu explorador de archivos a la izquierda se creará mágicamente el archivo requirements.txt.

<img width="417" height="27" alt="Foto5" src="https://github.com/user-attachments/assets/c492b4a8-c529-4478-8587-2b9497842f51" />

<img width="857" height="614" alt="FotoRequiments" src="https://github.com/user-attachments/assets/5c7d1901-6db9-4a66-b216-6fb5b5a5b34b" />

Seguido de aquello, en el directorio principal (la raíz de la carpeta que creamos al principio, al mismo nivel que requirements.txt), crearemos manualmente un archivo nuevo llamado Dockerfile. Es importante escribirlo tal cual, con la "D" mayúscula y sin ninguna extensión al final (nada de .txt ni .py).

¿Para qué sirve el Dockerfile? Piensa en el Dockerfile como el plano arquitectónico o la receta paso a paso para fabricar un computador virtual desde cero. Mientras que el requirements.txt solo lista las librerías de Python, el Dockerfile le da instrucciones completas al motor de Docker: le dice qué sistema operativo usar (como Linux), cómo copiar nuestra carpeta de proyecto hacia adentro del contenedor, cómo instalar el requirements.txt y, finalmente, qué comando usar para encender el servidor Uvicorn.

En otras palabras, este archivo vendría siendo las instrucciones de arranque. Una vez creado el archivo, copia y pega este código:

Dockerfile
# 1. IMAGEN BASE: Traemos un sistema operativo (Linux) ligero que ya trae Python 3.10 instalado.
# De esta manera prevenimos que el sistema no tenga python.
FROM python:3.10-slim

# 2. DIRECTORIO DE TRABAJO: Creamos una carpeta llamada /app dentro del contenedor y nos movemos ahí.
# Con este comando indicamos en qué carpeta trabajar.
WORKDIR /app

# 3. COPIAR DEPENDENCIAS: Copiamos solo el archivo requirements.txt primero.
# Con esto indicamos de dónde descargar las dependencias guardadas.
COPY requirements.txt .

# 4. INSTALAR DEPENDENCIAS: Ejecutamos pip para instalar lo que dice el archivo.
RUN pip install --no-cache-dir -r requirements.txt

# 5. COPIAR EL CÓDIGO: Copiamos todo el resto de los archivos de nuestro proyecto a la carpeta /app del contenedor.
# Por qué: Ahora que el entorno está listo, metemos nuestra aplicación (main.py).
COPY . .

# 6. PUERTO: Le decimos a Docker qué puerto usará la aplicación (libre elección).
EXPOSE 10000

# 7. COMANDO DE EJECUCIÓN: El comando exacto que encenderá el servidor cuando el contenedor se despierte.
# Por qué: Usa Uvicorn para correr el archivo main.py en el puerto 10000, accesible desde cualquier IP (0.0.0.0).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
Con este archivo lo que hacemos es que cada vez que arranquemos con docker siga estas instrucciones. Al final dice que iniciará en el puerto localhost:10000 (puedes cambiarlo a preferencia).

<img width="301" height="285" alt="Foto6" src="https://github.com/user-attachments/assets/0bfa7613-2629-4d62-aad4-5a632aad5234" />


4. Escribir el código y empaquetar la aplicación
Ahora que tenemos nuestras herramientas instaladas, vamos a escribir nuestra primera API. En la raíz de tu proyecto (al mismo nivel que tu Dockerfile y requirements.txt), crea un nuevo archivo llamado main.py y copia exactamente el siguiente código:

Python
from fastapi import FastAPI

# Inicializamos la aplicación
app = FastAPI()

# Creamos nuestra primera ruta web (la página principal)
@app.get("/") 
def read_root():
    return {"mensaje": "¡Mi entorno en la nube está funcionando perfectamente!"}
¿Qué hace este código? Básicamente, le dice a Python: "Crea un servidor web y, cuando alguien entre a la dirección principal (/), respóndele entregando este mensaje en formato de datos (JSON)".

<img width="818" height="368" alt="Foto7" src="https://github.com/user-attachments/assets/4a7f5bdf-5695-4ae0-b5ef-a6ee28c79546" />

Para que este código funcione, lo vamos a encapsular usando Docker. Abre tu terminal (asegúrate de estar en la carpeta de tu proyecto) y escribe este comando:

PowerShell
docker build -t mi-prueba-local .
¿Qué significa este comando?

build: Le dice a Docker que empiece a construir.

-t mi-prueba-local: Le asigna un nombre o "etiqueta" (tag) a tu creación para que sea fácil de encontrar.

.: Le indica a Docker que busque el archivo Dockerfile en la carpeta actual.

Este comando fabricará una Imagen de Docker. Una "imagen" no es un programa corriendo; piénsalo como una fotografía exacta o un molde de fábrica. Son los preparativos sellados y listos para ser desplegados. Una vez que termine el proceso, incluso podrás ver esta imagen guardada en la interfaz gráfica de tu Docker Desktop.

<img width="966" height="265" alt="Foto8" src="https://github.com/user-attachments/assets/24eb6910-7fca-45e0-a530-5e4acf352bf1" />

<img width="1050" height="391" alt="Foto10" src="https://github.com/user-attachments/assets/f296e694-8b17-42b2-94c7-8caa72fcc05d" />

5. Encender el contenedor y probar los Puertos
Ahora que tenemos el "molde" (la imagen), vamos a darle vida creando un Contenedor (el programa corriendo). Ejecuta el siguiente comando en tu terminal:

PowerShell
docker run -p 10000:10000 mi-prueba-local
Nota: Asegúrate de usar el guion - en mi-prueba-local, exactamente como lo nombraste en el paso anterior.

Explicación: ¿Qué es el -p 10000:10000? Esto se llama "Mapeo de Puertos" y es clave en el desarrollo web.

Imagina que el contenedor de Docker es un edificio cerrado herméticamente y tu computador (Host) es la calle de afuera.

El número de la derecha (10000) es la puerta por donde sale la información dentro del contenedor (porque así lo configuramos en el Dockerfile).

El número de la izquierda (10000) es la puerta que abres en tu computador físico para conectarte a ese edificio.

Dato útil: Puedes cambiar el número de la izquierda si quieres. Si escribes -p 8080:10000, la aplicación seguirá funcionando igual, pero tendrás que entrar desde tu navegador usando el puerto 8080.

<img width="881" height="116" alt="Foto11" src="https://github.com/user-attachments/assets/ffc308b3-676a-4b38-94fc-aa673a191e56" />

La prueba final: Con el contenedor corriendo, abre tu navegador web favorito y en la barra de direcciones escribe exactamente esto:

http://localhost:10000

Nota: Escribe http://, sin la "s" al final. localhost simplemente significa "mi propio computador".

Si todo salió bien, en la pantalla de tu navegador aparecerá el texto de tu código. Además, si miras la terminal de VS Code, verás que el servidor responde con mensajes que dicen 200 OK, lo cual en el lenguaje de internet significa que la conexión fue exitosa y sin errores.

<img width="895" height="298" alt="Foto12" src="https://github.com/user-attachments/assets/4e4a876a-5a95-41f1-9bd7-c040206ffab2" />


6. Configuración de automatización con GitHub Actions
¿Qué es y para qué sirve GitHub Actions? En el desarrollo profesional, cuando trabajas en equipo y subes tu código a internet para desplegarlo en producción, necesitas estar 100% seguro de que no vas a romper nada. GitHub Actions es una funcionalidad de automatización (conocida en la industria como CI/CD o Integración Continua). Funciona como un "robot vigilante": cada vez que subes código nuevo, este robot lee tus instrucciones, crea un servidor temporal en la nube, y comprueba que tu código realmente funcione y pueda construirse sin errores. Si el código está roto, el robot te avisa con una alerta roja antes de que ese error llegue a los usuarios finales.

Paso a paso para configurarlo:
Para que GitHub sepa qué tareas automatizar, debemos crear una estructura de carpetas muy específica, ya que GitHub buscará estas carpetas de forma automática.

En el directorio raíz de tu proyecto, crea una carpeta llamada .github (no olvides el punto al inicio).

Dentro de esa nueva carpeta, crea otra carpeta llamada workflows (en minúsculas y en plural).

Seguido de aquello, dentro de la carpeta workflows, crearemos un archivo con extensión .yml (YAML, un formato de texto muy estricto usado para configuraciones) que se llamará build.yml.

Abre ese archivo y copia y pega el siguiente código:

YAML
name: Comprobar Construccion de Docker

# Instrucciones de activación (cuando se haga push)
on:
  push:
    branches: [ "main", "master" ] # Se activa cuando subes código a la rama principal

# Pasos a seguir por el robot
jobs:
  build:
    runs-on: ubuntu-latest # El robot usará un servidor prestado con Linux (Ubuntu)

    steps:
    # Paso A: El robot descarga tu código desde tu repositorio
    - name: Obtener el código
      uses: actions/checkout@v3

    # Paso B: El robot intenta armar la caja fuerte usando tu Dockerfile
    - name: Construir imagen de Docker
      run: docker build -t mi-app-nube .
¿Qué le estamos diciendo a GitHub con esto? Le estamos dando dos indicaciones principales:

Cuándo actuar (on: push): "Cada vez que alguien empuje (push) código nuevo a la rama principal de este repositorio, despierta al robot".

Qué hacer (jobs: build): "Préstame un computador con Linux por un par de minutos, descarga mi código ahí, y ejecuta el comando de Docker para ver si la imagen se construye correctamente o si explota".

¿Cómo probar si funciona? Para verificar que todo está correcto, sube todos los cambios de tu proyecto a tu repositorio de GitHub usando los comandos habituales de Git (git add ., git commit -m "...", git push).

Una vez que el código esté subido, ve a la página de tu repositorio en la web de GitHub. En el menú superior, busca la pestaña que dice "Actions" (Acciones). Dentro de ahí, verás una lista con las ejecuciones de tu robot. Si tu código y tu Dockerfile están perfectos, verás la ejecución marcada con un hermoso círculo verde con un ticket (éxito). Si algo falló, aparecerá una cruz roja para que puedas revisar el error.

<img width="1302" height="390" alt="Foto13" src="https://github.com/user-attachments/assets/bdcdaaab-54f6-4939-838a-e9a9afa47ea1" />

7. Configuración de Supabase (Base de Datos y API Automática)
¿Qué es Supabase y por qué lo usamos? Supabase es una plataforma en la nube (Backend-as-a-Service) que funciona sobre una base de datos PostgreSQL. Su mayor ventaja es que, en el instante en que creas una tabla, Supabase genera automáticamente una API REST completa para ella. Esto significa que no tienes que escribir el código para hacer consultas (CRUD); Supabase te da las URLs listas para usar.

Paso A: Crear el proyecto y la tabla

Crea una cuenta gratuita en Supabase y selecciona "New Project". Asigna un nombre a tu base de datos y crea una contraseña segura.

Una vez dentro de tu panel, tienes dos opciones para crear tu tabla: usar la interfaz gráfica (en el menú izquierdo Table Editor) o usar código SQL directo.

<img width="830" height="552" alt="Foto16" src="https://github.com/user-attachments/assets/3909df5e-73f8-4eb6-92d4-c74b0f3d7894" />

<img width="982" height="449" alt="Foto18" src="https://github.com/user-attachments/assets/7e50c142-e8c9-4380-bd4b-ab46fbe91ec7" />

Para ir más rápido y con mayor precisión, ve al menú SQL Editor, pega el siguiente código y presiona "Run" para crear la estructura de la tabla:

SQL
CREATE TABLE public."PERSONAJE" (
  id_personaje bigint generated by default as identity not null,
  nombre character varying null,
  juego character varying null,
  sexo character varying null,
  imagen text null,
  constraint PERSONAJE_pkey primary key (id_personaje)
) TABLESPACE pg_default;
Paso B: Insertar un registro de prueba Seguido de aquello, le agregaremos un registro a nuestra tabla para tener datos que consultar. Borra el código anterior en el SQL Editor, pega este nuevo comando y presiona "Run":

SQL
INSERT INTO "public"."PERSONAJE" ("id_personaje", "nombre", "juego", "sexo", "imagen") 
VALUES (1, 'Lilith', 'Darkstalker', 'Mujer', '[https://upload.wikimedia.org/wikipedia/en/9/9d/Lilith_Aensland.png](https://upload.wikimedia.org/wikipedia/en/9/9d/Lilith_Aensland.png)');
Paso C: Obtener tus credenciales de conexión (URL y Key) Para que nuestro programa de Python (o Postman) pueda entrar a esta base de datos, necesita la dirección exacta y la llave de la puerta.

En la barra lateral izquierda, baja hasta el ícono del engranaje que dice Project Settings (Configuración del proyecto).

En el submenú que se abre, selecciona API.

En esta pantalla, copia dos cosas fundamentales y guárdalas en un bloc de notas:

Project URL: La dirección base de tu proyecto.
<img width="1242" height="592" alt="Foto14" src="https://github.com/user-attachments/assets/c898c110-64a2-430a-a8cd-6af49e5cb4c2" />

Project API Keys: Busca la clave que tiene la etiqueta verde anon y public. Esta es tu llave de acceso.
<img width="998" height="249" alt="Foto15" src="https://github.com/user-attachments/assets/05c5b065-1a02-4638-986b-fca0588dc63e" />


Nota de seguridad: Para los fines de este documento introductorio, haremos consultas directas con la llave anon. Sin embargo, en proyectos reales a nivel profesional o universitario, es obligatorio activar y configurar las políticas RLS (Row Level Security) en Supabase para proteger los datos de accesos no autorizados.

Paso D: Probar la conexión en Postman Antes de programarlo en Python, siempre es buena práctica probar si la API de Supabase nos responde directamente usando Postman.

Abre Postman y crea una nueva petición tipo GET.

En la barra de direcciones de Postman, arma tu URL uniendo la Project URL que copiaste, seguida de /rest/v1/ y el nombre exacto de tu tabla. Quedará algo así: https://izlcprswslrsmunpklny.supabase.co/rest/v1/PERSONAJE

El paso clave (Los Headers): Supabase no deja entrar a cualquiera. Debajo de la URL, ve a la pestaña Headers (Cabeceras).

En la columna Key, escribe exactamente la palabra: apikey

En la columna Value, pega la llave larguísima que copiaste en el paso anterior.

Presiona el botón azul Send.

Si seguiste los pasos correctamente, en la parte inferior de Postman verás aparecer un JSON perfectamente estructurado con los datos de Lilith que ingresaste en el Paso B. ¡Esto confirma que tu base de datos está viva y conectada a internet!

<img width="933" height="633" alt="FOTO22" src="https://github.com/user-attachments/assets/cc57a3cc-8985-4a14-acb2-cecfc086dac4" />

8. Configuración de Variables de Entorno (.env)
Para conectar nuestra API con Supabase de forma segura, crearemos un archivo llamado .env en la carpeta raíz del proyecto.

Nota: Este paso es una práctica estándar de ciberseguridad. Nunca debes escribir tus contraseñas directamente en el código de Python, especialmente si vas a subir este proyecto a repositorios públicos como GitHub.

Dentro de este archivo, escribiremos dos variables para guardar nuestra URL y nuestra llave secreta, sin espacios alrededor del signo igual:

Plaintext
SUPABASE_URL=[https://izlcprswslrsmunpklny.supabase.co](https://izlcprswslrsmunpklny.supabase.co)
SUPABASE_KEY=tu_llave_larga_aqui...
Muy importante: Si vas a usar GitHub, asegúrate de crear también un archivo llamado .gitignore y escribir .env dentro de él. Así evitarás que tu llave secreta se suba a internet por accidente.

9. Programación de la API hacia Supabase
Lo primero será instalar dos nuevas herramientas en nuestro entorno virtual (venv). En la terminal escribiremos:

PowerShell
pip install requests python-dotenv
¿Para qué sirven?

requests: Es el "mensajero". Le da a Python la capacidad de salir a internet, tocar la puerta de Supabase y traer los datos.

python-dotenv: Es el "lector de secretos". Su trabajo es leer el archivo .env que creamos antes y pasarle las contraseñas a Python de forma invisible.

Una vez instaladas, no olvides actualizar tu lista de requerimientos ejecutando:

<img width="789" height="139" alt="Foto20" src="https://github.com/user-attachments/assets/edebcbcc-c1f7-49e3-8da7-2442046c031b" />

PowerShell
pip freeze > requirements.txt
Después, abre tu archivo main.py, borra lo que tenías y pega este nuevo código:

Python
from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

# 1. Le decimos a Python que lea el archivo .env y cargue los secretos en memoria
load_dotenv()

app = FastAPI()

# 2. Creación de la ruta web
@app.get("/api/personajes")
def obtener_personajes():
    
    # Variable que guarda la URL de Supabase apuntando a nuestra tabla
    url_supabase = f"{os.getenv('SUPABASE_URL')}/rest/v1/PERSONAJE"
    
    # Obtenemos la contraseña desde el archivo .env
    mi_llave = os.getenv("SUPABASE_KEY")
    
    # Armamos el diccionario con las cabeceras de seguridad requeridas por Supabase
    cabeceras = {
        "apikey": mi_llave,
        "Authorization": f"Bearer {mi_llave}"
    }
    
    # Hacemos la llamada HTTP (método GET) a Supabase
    respuesta = requests.get(url_supabase, headers=cabeceras)
    
    # Devolvemos el resultado transformado en formato JSON
    return respuesta.json()

<img width="739" height="602" alt="FOTO21" src="https://github.com/user-attachments/assets/50fbf118-1020-46da-b8a4-f092154222be" />

10. Ejecutar la API: Desarrollo vs. Docker
Tienes dos formas de encender este proyecto, dependiendo de lo que necesites hacer:

Opción A: Modo Desarrollo Rápido (Uvicorn local) Ideal para cuando estás escribiendo código y quieres ver los cambios al instante. Ejecuta:

PowerShell
uvicorn main:app --reload
Esto iniciará el servidor en el puerto por defecto de Uvicorn. Para probarlo en Postman, usarás la URL: http://localhost:8000/api/personajes

Opción B: Modo Empaquetado (Docker) Ideal para comprobar que la "caja fuerte" funciona antes de subirla a la nube. Primero construyes la imagen y luego corres el contenedor inyectándole el archivo secreto:

PowerShell
docker build -t mi-prueba-local .       
docker run --env-file .env -p 10000:10000 mi-prueba-local     
Como aquí definimos manualmente los puertos (-p 10000:10000), para probarlo en Postman usarás la URL: http://localhost:10000/api/personajes

<img width="924" height="572" alt="FOTO23" src="https://github.com/user-attachments/assets/30ce09d5-d819-47ce-96ac-6734dc5d4374" />

11. Visualización Gráfica en Postman
Si quieres ver los datos JSON de manera gráfica y amigable en Postman, puedes inyectar un poco de código HTML y CSS.

Ve a la pestaña Tests (o Scripts -> Post-response) en Postman y pega este código:

JavaScript
var template = `
    <style>
        body { font-family: Arial, sans-serif; background-color: #222; color: white; padding: 20px; }
        .tarjeta { background: #333; border-radius: 10px; padding: 15px; width: 250px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }
        .tarjeta img { max-width: 100%; border-radius: 8px; margin-top: 10px; }
    </style>
    
    <h2>Personajes en la Base de Datos</h2>
    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
        {{#each respuesta}}
            <div class="tarjeta">
                <h3>{{nombre}}</h3>
                <p class="juego">Juego : {{juego}}</p>
                <p> Sexo: {{sexo}}</p>
                <img src="{{imagen}}" alt="Imagen de {{nombre}}" />
            </div>
        {{/each}}
    </div>
`;

// Renderizamos la plantilla usando los datos JSON de la respuesta
pm.visualizer.set(template, {
    respuesta: pm.response.json()
});
Presiona el botón "Send" y, en la parte inferior donde suele salir el JSON, haz clic en la pestaña Visualize. Verás una tarjeta gráfica con la foto de tu personaje generada a partir de los datos de Supabase.

<img width="906" height="486" alt="FotoFinal" src="https://github.com/user-attachments/assets/c79381c0-361f-48fb-8388-5299e685a777" />

12. Portabilidad (Trabajo en equipo)
Cuando trabajas en equipo, por ejemplo integrando el frontend de la plataforma web de gasfíteres con esta base de datos, es vital que tu compañero pueda levantar esta misma API en su propio computador sin tener que programar todo desde cero.

Gracias a las herramientas que configuramos, otra persona solo debe seguir estos 4 pasos rápidos para tener el proyecto funcionando en su máquina:

Clonar el proyecto: Descargar el código desde tu repositorio.
git clone url-de-tu-repositorio

Crear su propio entorno seguro: Tu compañero debe crear un archivo .env vacío en su computador y tú debes pasarle las credenciales (URL y Key) por un canal seguro para que las pegue ahí.

Replicar la burbuja: Tu compañero ejecuta:
python -m venv venv
.\venv\Scripts\activate

Instalar dependencias: Descarga exactamente las mismas versiones que tú usaste:
pip install -r requirements.txt

¡Y listo! Ya puede ejecutar el código y el entorno funcionará exactamente igual que en tu computador.
