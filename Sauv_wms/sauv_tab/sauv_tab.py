#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# NTL-SysToolbox - Export d'une table MySQL en CSV + rapport JSON

import csv
import json
import os
import sys
import getpass
from datetime import datetime

try:
    import pymysql
except ImportError:
    print("[ERREUR] pymysql n'est pas installé. Lancez setup.py")
    sys.exit(1)
    
def connect_to_database():
    """Demande les infos de connexion et retourne (connexion, base, host, port)."""
    print("\n--- Connexion MySQL ---\n")

    # Valeurs par défaut récupérées depuis l'environnement ou définies ici
    default_host = os.getenv("NTL_DB_HOST", "localhost")
    default_port = os.getenv("NTL_DB_PORT", "3306")
    default_user = os.getenv("NTL_DB_USER", "mspr")
    default_db = os.getenv("NTL_DB_NAME", "WMS")

    host = input(f"  Hôte / IP [{default_host}] : ").strip() or default_host
    port_str = input(f"  Port      [{default_port}] : ").strip() or default_port
    user = input(f"  User      [{default_user}] : ").strip() or default_user
    password = os.getenv("NTL_DB_PASSWORD") or getpass.getpass("  Password                 : ")
    database = input(f"  Base      [{default_db}] : ").strip() or default_db

    try:
        port = int(port_str)
    except ValueError:
        print("  [ERREUR] Le port doit être un nombre.")
        sys.exit(1)

    try:
        # Connexion à la base MySQL distante ou locale
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.Cursor,
            connect_timeout=10,
            autocommit=False
        )
        print("  Connexion OK !\n")
        return conn, database, host, port

    except pymysql.MySQLError as e:
        print(f"  [ERREUR] Connexion MySQL impossible : {e}")
        sys.exit(1)

def choose_table(conn):
    """Affiche les tables et retourne celle choisie par l'utilisateur."""
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        print("  [ERREUR] Aucune table trouvée.")
        sys.exit(1)

    print("  Tables disponibles :\n")
    for i, table_name in enumerate(tables, 1):
        print(f"    {i}. {table_name}")

    choice = input("\n  Numéro ou nom : ").strip()

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(tables):
            return tables[index]

    if choice in tables:
        return choice

    print("  [ERREUR] Choix invalide.")
    sys.exit(1)


def save_table_to_CSV():
    """Fonction principale."""
    print("\n" + "=" * 50)
    print("   NTL-SysToolbox - Sauvegarde table en CSV")
    print("=" * 50)

    conn, database, host, port = connect_to_database()

    try:
        table = choose_table(conn)

        # Dossier où seront générés le CSV et le rapport JSON
        default_output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "exports"
        )
        output_dir = input(f"\n  Dossier [{default_output_dir}] : ").strip() or default_output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Lecture complète de la table sélectionnée
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `{table}`;")
            rows = cursor.fetchall()
            headers = [col[0] for col in cursor.description]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Création du fichier CSV
        csv_path = os.path.join(output_dir, f"export_{table}_{timestamp}.csv")
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as csv_file:
            csv_file.write(
                f"# TABLE : {table} | BASE : {database} | HOTE : {host} | PORT : {port} | "
                f"DATE : {export_date} | LIGNES : {len(rows)}\n"
            )
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(headers)
            writer.writerows(rows)

        # Création du rapport JSON de traçabilité
        json_path = os.path.join(output_dir, f"report_{table}_{timestamp}.json")
        report_data = {
            "module": "sauv_tab",
            "status": "success",
            "host": host,
            "port": port,
            "database": database,
            "table": table,
            "rows_exported": len(rows),
            "columns": headers,
            "csv_file": csv_path,
            "generated_at": datetime.now().isoformat()
        }

        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(report_data, json_file, indent=4, ensure_ascii=False)

        print("\n" + "=" * 50)
        print("  Export réussi !")
        print(f"  Serveur : {host}:{port}")
        print(f"  Base    : {database}")
        print(f"  Table   : {table}")
        print(f"  CSV     : {csv_path}")
        print(f"  JSON    : {json_path}")
        print(f"  Lignes  : {len(rows)}")
        print(f"  Colonnes: {', '.join(headers)}")
        print("=" * 50 + "\n")

    finally:
        conn.close()


if __name__ == "__main__":
    save_table_to_CSV()
