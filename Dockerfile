# Usa una imagen de Python
FROM python:3.11.6

# Establece el directorio de trabajo en /app
WORKDIR /app

RUN apt update && apt upgrade -y
# Copia el archivo de requisitos al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el script de Python al contenedor
COPY . .

# Ejecuta el script cuando el contenedor se inicia
CMD ["bash", "start.sh"]
