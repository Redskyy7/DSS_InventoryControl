import psycopg2

def criar_banco(db_config):
    conn = psycopg2.connect(
        dbname=db_config["database"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"]
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_config['database']}'")
    existe = cursor.fetchone()
    
    if not existe:
        cursor.execute(f"CREATE DATABASE {db_config['database']}")
        print(f"Banco de dados '{db_config['database']}' criado com sucesso!")
    
    cursor.close()
    conn.close()