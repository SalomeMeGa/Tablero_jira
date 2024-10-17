from objetos import objeto
from tickets import ticket

    # Biblioteca utilizada para la manipulación de datos en forma de Dataframes.
import pandas as pd
from config import Config
    #Importa el conector de MySQL para conectarse a una base de datos MySQL
import mysql.connector
    #Biblioteca para manejar la serialización de datos en formato JSON.
import json
    #Importa datatime para manejar fechas y horas.
from datetime import datetime

    #Función que establece la conexión con la base de datos MySQL
def get_mysql_connection():
    # Detalles de configuración proporcionados por la clase Config
    config = {
        "user": Config.mysql_user,
        "password": Config.mysql_password,
        "host": Config.mysql_host,
        "port": Config.mysql_port,
        "database": Config.mysql_db,
    }
    try:
        # Conexión a la base de datos
        conn = mysql.connector.connect(**config)
        return conn
        #Fallo de conexión a la base de datos.
    except mysql.connector.Error as e:
        print(f"Error en la conexión: {e}")
        return None

        # Verifica si existen datos en la tabla de la base de datos
def check_data_exists(conn, table_name):
    try:
        mysql_table = Config.mysql_table
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM {mysql_table} "   #<- Realiza una consulta para contarlos registros en la tabla y devuelve true si hay registros
        cursor.execute(query)                            #<-Ejecuta la consulta construida anterior, utilizando el cursor de la conexión. Cursor "Es un objeto""
        result = cursor.fetchone()                       #<-Recupera una fila del resultado de la consulta ejecutada
        cursor.close()                                   #<-Cierra el cursor una vez que se ha obtenido resultado.


        return result[0] > 0                             #<-Si el valor existe, el resultado será mayor que 0
    except mysql.connector.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return False

        #Es utilizada en un entorno de AWS Lambda que combina, procesa y guarda datos en una base de datos MySQL y CSV
def lambda_handler(event, context):

    df = objeto()        #Obtención de datos <llamar a la función objeto y ticket>
    df2 = ticket()


    merged_df = pd.merge(df2, df, on='CRDD')                  #<-Se realiza el merge entre los DataFrames, con el campo CRDD existente en ambas tablas
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M')  #<-Se crea una variable para guardar la fecha y hora actual
    merged_df['fecha_modificacion'] = fecha_actual            #<-Añade una columna fecha_modificacion con la fecha y hora actuales.

    merged_df.to_csv('reporte_general.csv',index=False)       #<-Guardas en un archivo CSV del merge final "OPCIONAL"

    # Se conecta a la base de datos
    conn = get_mysql_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()


            mysql_table = Config.mysql_table                    #<-Obtiene el nombre de la tabla en la base de datos desde la configuración
            # Genera una cadena de texto con los nombres de las columnas del Dataframe merge_df, y cada una encerrada en " ' "

            columns = ', '.join([f"`{col}`" for col in merged_df.columns])               #<- merge_df.columns: obtiene la lista de columnasa de Dataframe, separados ´por " , "
            values = ', '.join(['%s'] * len(merged_df.columns))                          #<-Crea una cadena de placeholders %s para los valores que se insertaran en la tabla

            insert_query = f"INSERT INTO {mysql_table} ({columns}) VALUES ({values})"    #<-Crea la consulta SQL para insertar datos en la tabla mysql_table, usando los nombres de las columnas y los placeholders
            delete_query = f"DELETE FROM {mysql_table}"                                  #<-Crea una consulta SQL para eliminar todos los registros de la tabla mysql_table
                                                                                        #Esta consulta limpia la tabla antes de insertar nuevos datos
            data = [tuple(row) for row in merged_df.to_numpy()]                          #<- Convierte cada fila del Dataframe merge_df a una tupla
                                                                                        #<-merged_df.to_numpy(), convierte el dataframe en un array de Numpy, y luego se itera sobre cada fila para crea las lista de tuplas
            # Eliminación de los datos existentes si hay registros
            if check_data_exists(conn, mysql_table):
                cursor = conn.cursor()                                               #<-Se crea un cursor, se ejecuta la consulta de eliminación y luego se cierra el cursor.
                cursor.execute(delete_query)
                cursor.close()

            # Inserción de los nuevos datos
            cursor = conn.cursor()
            cursor.executemany(insert_query, data)
            cursor.close()
            #Confirmación de los cambios en la base de datos
            conn.commit()
            conn.close()
            #Manejo de excepciones
        except mysql.connector.Error as e:
            print(f"Error al enviar a la base de datos: {e}")
            conn.close()
            return {
                'statusCode': 500,
                'body': 'Error al enviar a la base de datos'
            }

    return {
        'statusCode': 200,
        'body': json.dumps(merged_df.to_dict(orient='records'))  # Si se regresa un 200 el cuerpo de la respuesta incluye los datos del dataframe merge_df convertidos a una lista de diccionarios
    }

# Ejecuta la función lambda
if __name__ == '__main__':
    lambda_handler(None, None)