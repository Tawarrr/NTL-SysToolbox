import pymysql

def connect_to_database():
    print("\n--- Connexion MySQL ---")
    host = input("  Hôte / IP  : ").strip() or "WMS-APP"
    user = input("  User [mspr] : ").strip() or "mspr"
    password = getpass.getpass("  Password : ") # mspr
    database = input("  Base [WMS] : ").strip() or "WMS"

    try:
        # Connexion classique sans options de curseur spéciales
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306,
            connect_timeout=10
        )
        print("Connexion OK !\n")
        return conn
    except Exception as e:
        print(f"[ERREUR] : {e}")
        return None
