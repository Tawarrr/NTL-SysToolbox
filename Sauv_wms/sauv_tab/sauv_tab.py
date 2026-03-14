import csv
import os
import getpass
import pymysql
from datetime import datetime

def connect_to_database():
    print("\n--- Connexion MySQL ---")
    host = input("  Hôte / IP  : ").strip() or "WMS-APP"
    user = input("  User [mspr] : ").strip() or "mspr"
    password = getpass.getpass("  Password : ")
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

def save_table_to_CSV():
    conn = connect_to_database()
    if not conn:
        return

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
            return
        
        table = tables[int(choice) - 1]

        # 2. Préparation du fichier
        os.makedirs("exports", exist_ok=True)
        path = f"exports/export_{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # 3. Exportation simple
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM `{table}`;")
            
            # Récupère tout d'un coup en mémoire
            lignes = cur.fetchall()
            colonnes = [desc[0] for desc in cur.description]

            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(colonnes)  # Écrit les colonnes
                writer.writerows(lignes)    # Écrit toutes les lignes d'un coup

        print(f"\n✅ Terminé ! {len(lignes)} lignes dans {path}")

    except Exception as e:
        print(f"[ERREUR] : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    save_table_to_CSV()
