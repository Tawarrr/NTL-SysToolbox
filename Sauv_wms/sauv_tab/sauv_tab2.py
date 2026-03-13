import csv
import json
import os
import getpass
import pymysql
from datetime import datetime

def connect_to_database():
    """Gère la connexion sécurisée et retourne l'objet connexion."""
    print("\n--- Connexion MySQL ---")

    host = input(f"  Hôte / IP  : ").strip() or "WMS-APP"
    user = input(f"  User [mspr] : ").strip() or "mspr"
    password = getpass.getpass("  Password : ") # mspr
    database = input(f"  Base [WMS] : ").strip() or "WMS"

    try:
        # SSCursor est crucial pour le distant : il lit ligne par ligne sans saturer la RAM
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306,
            cursorclass=pymysql.cursors.SSCursor,
            connect_timeout=10
        )
        print("Connexion OK !\n")
        return conn, database, host
    except Exception as e:
        print(f"[ERREUR] Connexion impossible : {e}")
        return None, None, None

def save_table_to_CSV():
    """Fonction appelée par le menu principal pour l'export CSV."""
    conn, database, host = connect_to_database()
    if not conn:
        return

    try:
        # 1. Sélection de la table
        # On utilise un curseur temporaire classique juste pour lister les tables
        with conn.cursor(pymysql.cursors.Cursor) as cur:
            cur.execute("SHOW TABLES;")
            tables = [row[0] for row in cur.fetchall()]

        if not tables:
            print("  [ERREUR] Aucune table trouvée.")
            return

        print("  Tables disponibles :")
        for i, table_name in enumerate(tables, 1):
            print(f"    {i}. {table_name}")

        choice = input("\n  Numéro de la table : ").strip()
        table = tables[int(choice) - 1] if choice.isdigit() and 0 < int(choice) <= len(tables) else None

        if not table:
            print("  [ERREUR] Choix invalide.")
            return

        # 2. Préparation des dossiers et fichiers
        output_dir = os.path.join(os.getcwd(), "exports")
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = os.path.join(output_dir, f"export_{table}_{timestamp}.csv")

        # 3. Exportation en flux (Streaming)
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM `{table}`;")
            headers = [desc[0] for desc in cur.description]

            with open(csv_path, "w", newline="", encoding="utf-8-sig") as csv_file:
                writer = csv.writer(csv_file, delimiter=";")
                writer.writerow(headers) # En-têtes

                print(f"  Transfert de la table '{table}' en cours...")
                count = 0
                while True:
                    row = cur.fetchone()
                    if not row: break
                    writer.writerow(row)
                    count += 1

        print("\n" + "=" * 40)
        print(f"  Export réussi !")
        print(f"  Fichier : {csv_path}")
        print(f"  Lignes  : {count}")
        print("=" * 40)

    except Exception as e:
        print(f"[ERREUR DURANT L'EXPORT] : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    save_table_to_CSV()
