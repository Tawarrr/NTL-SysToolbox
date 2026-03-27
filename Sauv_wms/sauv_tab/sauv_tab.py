import csv, os, pymysql
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
def connect_to_database():
    print("\n--- Connexion MySQL ---")
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_MDP')
    database = os.getenv('DB_NAME')
    try:
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
        return False

def save_table_to_CSV():
    conn = connect_to_database()
    if not conn:
        return False

    try:
        # 1. Lister les tables
        with conn.cursor() as cur:
            cur.execute("SHOW TABLES;")
            tables = [ligne[0] for ligne in cur.fetchall()]

        print("  Tables disponibles :")
        for i, t in enumerate(tables, 1):
            print(f"    {i}. {t}")

        choice = input("\n  Numéro de la table : ").strip()
        if not choice.isdigit() or not (0 < int(choice) <= len(tables)):
            print("Choix invalide.")
            return False

        table = tables[int(choice) - 1]

        # 2. Préparation du fichier
        os.makedirs("exports", exist_ok=True)
        path = f"exports/export_{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # 3. Exportation simple
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM `{table}`;")
            lignes = cur.fetchall()
            colonnes = [desc[0] for desc in cur.description]

            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(colonnes)  # Écrit les colonnes
                writer.writerows(lignes)    # Écrit toutes les lignes

        print(f"Terminé ! {len(lignes)} lignes dans {path}")
        return True
    except Exception as e:
        print(f"[ERREUR] : {e}")
        return True
    finally:
        conn.close()

if __name__ == "__main__":
    save_table_to_CSV()
