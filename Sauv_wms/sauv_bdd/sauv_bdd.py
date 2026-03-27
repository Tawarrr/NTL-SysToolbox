import os, pymysql
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
        return conn, database
    except Exception as e:
        print(f"[ERREUR] : {e}")
        return None, None

def sauvegarder_bdd_sql():
    conn, nom_bd = connect_to_database()
    if not conn:
        return False

    #Préparation du fichier de sortie
    dossier = "backups_sql"
    os.makedirs(dossier, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"backup_{nom_bd}_{timestamp}.sql"
    chemin_complet = os.path.join(dossier, nom_fichier)

    try:
        print(f"Début de la sauvegarde de '{nom_bd}'...")

        with open(chemin_complet, 'w', encoding='utf-8') as f:
            f.write(f"-- Sauvegarde Base de données : {nom_bd}\n")
            f.write(f"-- Date : {datetime.now()}\n")
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

            with conn.cursor() as cur:
                # 2. Récupérer la liste des tables
                cur.execute("SHOW TABLES")
                tables = [t[0] for t in cur.fetchall()]

                for table in tables:
                    print(f"  -> Traitement de la table : {table}")

                    # 3. Sauvegarder la structure
                    cur.execute(f"SHOW CREATE TABLE `{table}`")
                    structure = cur.fetchone()[1]
                    f.write(f"\n-- Structure de la table `{table}`\n")
                    f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
                    f.write(f"{structure};\n\n")

                    # 4. Sauvegarder les données
                    cur.execute(f"SELECT * FROM `{table}`")
                    lignes = cur.fetchall()

                    if lignes:
                        f.write(f"INSERT INTO `{table}` VALUES ")
                        valeurs_sql = []
                        for l in lignes:
                            v_nettoyees = [f"""'{str(v).replace("'", "''")}'""" if v is not None else "NULL" for v in l]
                            valeurs_sql.append(f"({','.join(v_nettoyees)})")

                        f.write(",\n".join(valeurs_sql) + ";\n")

            f.write("\nSET FOREIGN_KEY_CHECKS = 1;")

        print(f"Sauvegarde réussie : {chemin_complet}")
        return True
    except Exception as e:
        print(f"Erreur pendant l'export : {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    sauvegarder_bdd_sql()
