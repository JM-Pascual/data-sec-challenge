import os
from dotenv import load_dotenv
import mysql.connector
from system_failure_report import (create_database,
                                   use_database,
                                   create_system_report_tables,
                                   load_system_report_tables,
                                   query_customers_with_max_failure_events)

if __name__ == '__main__':
    load_dotenv()

    # Establezco la conexión con la base de datos
    connection = mysql.connector.connect(
        user=os.getenv('DB_USER'),
        host=os.getenv('DB_HOST'),
        password=os.getenv('DB_PASSWORD')
    )

    cursor = connection.cursor()

    db_name = os.getenv('DB_NAME')

    # Creo la base de datos en caso de que no exista y la selecciono
    create_database(cursor, db_name)
    use_database(cursor, db_name)

    # Llamo a la funcion que crea las tablas del sistema segun es esquema dado
    create_system_report_tables(cursor)

    # Cargo los datos enunciados en la consigna en las tablas del sistema
    load_system_report_tables(cursor)

    # Llamo a la funcion que realiza la consulta solicitada
    query_customers_with_max_failure_events(cursor)

    # Cierro la conexión con la base de datos
    cursor.close()
    connection.close()

