# Usar una imagen base de Python 3.8
FROM python:3.8

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar todos los archivos al contenedor
COPY . .

# Instalar bibliotecas necesarias
RUN pip install pymongo
RUN pip install pandas

# Comando a ejecutar cuando el contenedor se inicie
CMD ["python", "main.py"]
