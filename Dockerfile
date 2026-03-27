# 1. IMAGEN BASE: Traemos un sistema operativo (Linux) ligero que ya trae Python 3.10 instalado.
# DE esta manera prevenimos de que el sistema no tenga python.
FROM python:3.10-slim

# 2. DIRECTORIO DE TRABAJO: Creamos una carpeta llamada /app dentro del contenedor y nos movemos ahí.
# Con este comando indicamos en que carpeta trabajar
WORKDIR /app

# 3. COPIAR DEPENDENCIAS: Copiamos solo el archivo requirements.txt primero.
# Con esto indicamos de donde descargar las dependencias guardadas
COPY requirements.txt .

# 4. INSTALAR DEPENDENCIAS: Ejecutamos pip para instalar lo que dice el archivo.
RUN pip install --no-cache-dir -r requirements.txt

# 5. COPIAR EL CÓDIGO: Copiamos todo el resto de los archivos de nuestro proyecto a la carpeta /app del contenedor.
# Por qué: Ahora que el entorno está listo, metemos nuestra aplicación (main.py).
COPY . .

# 6. PUERTO: Le decimos a Docker qué puerto usará la aplicación (libre elecion)
EXPOSE 10000

# 7. COMANDO DE EJECUCIÓN: El comando exacto que encenderá el servidor cuando el contenedor se despierte.
# Por qué: Usa Uvicorn para correr el archivo main.py en el puerto 10000, accesible desde cualquier IP (0.0.0.0).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]