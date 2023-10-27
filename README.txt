RPA (DATA)

Descripción:
script está diseñado para ser ejecutado como una tarea programada y puede ser fácilmente adaptado o extendido para satisfacer requisitos adicionales.

Prerrequisitos
Docker instalado en su máquina local.
Cuenta de AWS EC2.
Cuenta de Docker Hub.


Pasos para el Despliegue y Ejecución en AWS EC2

Paso 1: Preparar el entorno local
	abrir la carpeta y los archivos .py y .json que contien la prueba tecnica.

Paso 2: Construir la imagen de Docker
	Ejecutar docker build -t nombre_de_su_imagen .en el directorio del proyecto.

Paso 3: Subir la imagen a Docker Hub
	Ejecutar docker loginy proporcionar las credenciales de Docker Hub.
	Ejecutar docker tag nombre_de_su_imagen:latest su_usuario_de_docker/nombre_de_su_imagen:latest.
	Ejecutar docker push su_usuario_de_docker/nombre_de_su_imagen:latest.

Paso 4: Crear una instancia en AWS EC2
	Siga las instrucciones en la consola de AWS para lanzar una nueva instancia.

Paso 5: Conectarse a la instancia de AWS EC2
	Utilice SSH para conectarse a la instancia.

Paso 6: Instalar Docker en AWS EC2

Paso 7: Ejecutar los siguiente comando uno por uno

	sudo apt update
	sudo apt install docker.io -y
	sudo systemctl start docker
	sudo systemctl enable docker

Paso 8: Desplegar la aplicación

	Descargue la imagen de Docker con: 
	sudo docker pull su_usuario_de_docker/nombre_de_su_imagen.

	Ejecutar el contenedor con sudo docker:
	run su_usuario_de_docker/nombre_de_su_imagen.

Paso 9: (Opcional) Configurar Cron para Ejecución Automática
	Agregar la tarea programada con: 
	crontab -e.
	Para elejir en que periodos de tiempo se va a ejecutar el programa


licencia
Este proyecto RPA (DATA) fue creado por:
ELMER ESTEBAN MUÑOZ MARTINEZ