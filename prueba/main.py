import pymongo
import pandas as pd
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Leer las configuraciones desde el archivo JSON
# Esto incluye credenciales para MongoDB y correo electrónico
with open('config.json', 'r') as f:
    configuracion = json.load(f)

# Obtener las credenciales desde el archivo de configuración
mongo = configuracion.get('mongo')
email = configuracion.get('email')
email_password = configuracion.get('email_password')

def conexion():
    """
    Establece la conexión con MongoDB Atlas y retorna el cliente.

    Returns:
        pymongo.MongoClient: Cliente de la conexión MongoDB.
    """
    cliente = None
    try:
        cliente = pymongo.MongoClient(mongo)
        if cliente.server_info():
            print("Conexión exitosa a MongoDB Atlas")
    except pymongo.errors.ConnectionFailure as e:
        print(f"Error de conexión: {e}")
    except Exception as ex:
        print(f"Otro error: {ex}")
    return cliente

def consulta():
    """
    Realiza una consulta a la base de datos y retorna un DataFrame con los resultados.

    Returns:
        pd.DataFrame: DataFrame con los resultados de la consulta.
    """
    cliente = conexion()
    df = pd.DataFrame()  # Inicializar un DataFrame vacío
    if cliente is not None:
        try:
            db = cliente['bd-ejemplo']
            coleccion = db['pedidos']
            query = {'shipping_status': {'$in': ['returned', 'cancelled']}}
            proyeccion = {'order_vendor_dbname': 1, 'shipping_status': 1, 'shipping_date': 1, '_id': 0}
            cursor = coleccion.find(query, proyeccion)
            df = pd.DataFrame(list(cursor))
            df['mes'] = pd.to_datetime(df['shipping_date']).dt.month  # Extraer el mes
            # Agrupar los datos
            gropo_df = df.groupby(['order_vendor_dbname', 'mes', 'shipping_status']).size().reset_index(name='count')
            df = gropo_df[gropo_df['count'] >= 3]
        except Exception as e:
            print(f"Error en la consulta: {e}")
    return df

def alerta_email(df):
    """
    Envía un DataFrame como archivo CSV adjunto por correo electrónico.
    Args:
        df (pd.DataFrame): DataFrame a enviar.
    """
    try:
        archivo = "data.csv"
        df.to_csv(archivo, index=False)  # Guardar el DataFrame como un archivo CSV
        asunto = "Aleta Clientes con devoluciones y cancelados"
        descripcion = "Adjunto archivo con datos de clientes con más de 2 pedidos en estado de devolución o cancelado por mes."
        
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = "elmer.munoz171@pascualbravo.edu.co"  # Sustituir por el correo electrónico del destinatario
        msg["Subject"] = asunto
        msg.attach(MIMEText(descripcion, "plain"))

        # Adjuntar el archivo CSV
        with open(archivo, "rb") as f:
            adjuntar = MIMEApplication(f.read(), _subtype="csv")
            adjuntar.add_header("Content-Disposition", "attachment", archivo=str(archivo))
            msg.attach(adjuntar)

        # Configurar y enviar el correo
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, email_password)
        server.sendmail(email, "elmer.munoz171@pascualbravo.edu.co", msg.as_string())  # Sustituir por el correo electrónico del destinatario
        server.quit()
        print('Correo enviado con éxito.')
    except smtplib.SMTPException as e:
        print(f"Error al enviar el correo: {e}")

def alerta_insercion_db(df):
    """
    Inserta un DataFrame en una nueva colección de MongoDB.
    Args:
        df (pd.DataFrame): DataFrame a insertar.
    """
    cliente = conexion()
    if cliente is not None:
        try:
            db = cliente['bd-ejemplo']
            coleccion = db['alerta_cliente_pedido']
            data_dict = df.to_dict("records")  # Convertir el DataFrame a un diccionario
            coleccion.insert_many(data_dict)  # Insertar los registros
            print("Datos insertados con éxito.")
        except pymongo.errors.PyMongoError as e:
            print(f"Error en la inserción: {e}")

if __name__ == "__main__":
    # Realizar la consulta a la base de datos
    df_resultado = consulta()
    # Si el DataFrame no está vacío, enviar alertas
    if not df_resultado.empty:
        alerta_email(df_resultado)  # Enviar alerta por correo electrónico
        alerta_insercion_db(df_resultado)  # Insertar datos en una nueva colección de MongoDB