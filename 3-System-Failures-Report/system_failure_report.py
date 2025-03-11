def show_databases(cursor):
    cursor.execute("SHOW DATABASES")

    print("Databases:")
    for database in cursor:
        print(database[0])

def show_tables(cursor):
    cursor.execute("SHOW TABLES")

    print("Tables:")
    for table in cursor:
        print(table[0])

def show_table_content(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")

    print(f"Table {table_name} content:")
    columns = [desc[0] for desc in cursor.description]
    print("\t".join(columns))
    for row in cursor:
        print(row)

def create_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")

def drop_database(cursor, db_name):
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")

def use_database(cursor, db_name):
    cursor.execute(f"USE {db_name};")

def create_table(cursor, table_name, columns_data):
    columns_data_parsed = ", ".join(columns_data)
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} ({columns_data_parsed});""")

def insert_to_table(cursor, table_name, columns, values):
    columns_parsed = ", ".join(columns)
    for value in values:
        cursor.execute(f"""INSERT INTO {table_name} ({columns_parsed}) VALUES {value};""")

def create_system_report_tables(cursor):
    create_table(cursor, "customers", [
        "id SMALLINT PRIMARY KEY",
        "first_name VARCHAR(64) NOT NULL",
        "last_name VARCHAR(64) NOT NULL"
    ])

    create_table(cursor, "campaigns", [
        "id SMALLINT PRIMARY KEY",
        "customer_id SMALLINT NOT NULL",
        "name VARCHAR(64) NOT NULL",
        "FOREIGN KEY (customer_id) REFERENCES customers(id)"
    ])

    create_table(cursor, "events", [
        "dt VARCHAR(19)",
        "campaign_id SMALLINT NOT NULL",
        "status VARCHAR(64) NOT NULL",
        "FOREIGN KEY (campaign_id) REFERENCES campaigns(id)"
    ])

def load_system_report_tables(cursor):
    insert_to_table(
        cursor,
        "customers",
        ["id", "first_name", "last_name"],
        ["(1, 'Whitney', 'Ferrero')", "(2, 'Dickie', 'Romera')"]
    )

    insert_to_table(
        cursor,
        "campaigns",
        ["id", "customer_id", "name"],
        [
            "(1, 1, 'Upton Group')",
            "(2, 1, 'Roob, Hudson and Rippin')",
            "(3, 1, 'McCullough, Rempel and Larson')",
            "(4, 1, 'Lang and Sons')",
            "(5, 2, 'Ruecker, Hand and Haley')"
        ]
    )

    insert_to_table(
        cursor,
        "events",
        ["dt", "campaign_id", "status"],
        [
            "('2021-12-02 13:52:00', 1, 'failure')",
            "('2021-12-02 08:17:48', 2, 'failure')",
            "('2021-12-02 08:18:17', 2, 'failure')",
            "('2021-12-01 11:55:32', 3, 'failure')",
            "('2021-12-01 06:53:16', 4, 'failure')",
            "('2021-12-02 04:51:09', 4, 'failure')",
            "('2021-12-01 06:34:04', 5, 'failure')",
            "('2021-12-02 03:21:18', 5, 'failure')",
            "('2021-12-01 03:18:24', 5, 'failure')",
            "('2021-12-02 15:32:37', 1, 'success')",
            "('2021-12-01 04:23:20', 1, 'success')",
            "('2021-12-02 06:53:24', 1, 'success')",
            "('2021-12-02 08:01:02', 2, 'success')",
            "('2021-12-01 15:57:19', 2, 'success')",
            "('2021-12-02 16:14:34', 3, 'success')",
            "('2021-12-02 21:56:38', 3, 'success')",
            "('2021-12-01 05:54:43', 4, 'success')",
            "('2021-12-02 17:56:45', 4, 'success')",
            "('2021-12-02 11:56:50', 4, 'success')",
            "('2021-12-02 06:08:20', 5, 'success')"
        ]
    )

def execute_query(cursor, query):
    cursor.execute(query)

    print("Query result:")
    columns = [desc[0] for desc in cursor.description]
    print("\t".join(columns))
    for row in cursor:
        print(row)

# La siguiente query devuelve aquellos clientes que tengan mas de 3 eventos de tipo 'failure'
# Para lograrlo se joinean las tablas customers, campaigns y events utilizando las llaves que las relacionan
# Luego se filtran los eventos que tengan status 'failure' de las entradas resultantes
# Se agrupa por id de cliente y se filtra el resultado segun aquellos que tengan mas de 3 eventos de tipo 'failure'
# Finalmente se muestra el nombre completo del cliente y la cantidad de eventos de tipo 'failure' que tiene en dos columnas distintas
def query_customers_with_max_failure_events(cursor):
    execute_query(
        cursor,
        """
            SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer, COUNT(e.status) AS failures
            FROM customers c
            JOIN campaigns cp ON c.id = cp.customer_id
            JOIN events e ON cp.id = e.campaign_id
            WHERE e.status = 'failure'
            GROUP BY c.id, c.first_name, c.last_name
            HAVING COUNT(e.status) > 3;
        """)
