import pymysql

def connect_to_database():
    print ("Tentative de connexion à la base de données...")
    try:
        connection = pymysql.connect(
            host="localhost",
            user="Admin_WMS",
            password="PASSWORD",
            database="WMS"
        )
        print("Connection établie!")
        return connection
    except pymysql.MySQLError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None
    