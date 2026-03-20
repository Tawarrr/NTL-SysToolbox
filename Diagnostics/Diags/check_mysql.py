import os, pymysql
from dotenv import load_dotenv
load_dotenv()
def test_mysql_connection():
    print("\n--- Connexion MySQL (via PyMySQL) ---")
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_MDP')
    database = os.getenv('DB_NAME')

    connection = None

    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306,
            connect_timeout=10
        )


        # Utilisation d'un curseur pour récupérer les infos
        with connection.cursor() as cursor:
            # Récupérer la base actuelle
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"Actuellement connecté à la base : {db_name[0]}")
            print("La base de données MySQL est bien fonctionnelle.")

    except pymysql.MySQLError as e:
        print(f"\n[!] Erreur PyMySQL : {e}")
    except Exception as e:
        print(f"\n[!] Autre erreur : {e}")

    finally:
        # On ferme si l'objet connexion a bien été instancié
        if connection:
            connection.close()
            print("\nConnexion MySQL fermée.")

if __name__ == "__main__":
    test_mysql_connection()
