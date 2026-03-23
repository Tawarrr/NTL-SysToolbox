import mysql.connector, os, requests, time
from dotenv import load_dotenv
load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_MDP')
database = os.getenv('DB_NAME')

def nettoyer_nom_version(v):
    if not v: return v
    v = str(v).lower()
    # On coupe au premier tiret pour enlever -r2, -sac, -sp1
    v = v.split('-')[0]
    # On enlève les espaces inutiles
    return v.strip()

def maj_referentiel():
    print("Synchronisation EOL")
    produits = {
        'ubuntu': 'linux',
        'windows-server': 'windows-server'
    }

    try:
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = db.cursor()

        for api_name, db_os_name in produits.items():
            print(f"[*] Traitement de : {api_name}...")
            res = requests.get(f"https://endoflife.date/api/{api_name}.json")

            if res.status_code == 200:
                for entry in res.json():
                    # Nettoyage du cycle (Ex: 2012-r2 devient 2012)
                    v_majeure = nettoyer_nom_version(entry.get('cycle'))

                    # Le build/release (Ex: 10.0.20348 ou 20.04.6)
                    v_detail = str(entry.get('latest', ''))

                    date_eol = entry.get('eol')

                    if date_eol and date_eol is not False:
                        sql = """
                            INSERT INTO referentiel_eol (nom_os, version, version_detail, date_eol)
                            VALUES (%s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                date_eol = VALUES(date_eol),
                                version_detail = VALUES(version_detail)
                        """
                        cursor.execute(sql, (db_os_name, v_majeure, v_detail, date_eol))

                db.commit()
                print(f"[OK] {db_os_name} mis à jour.")
            time.sleep(0.5)

        db.close()
        print("\n[SUCCÈS] Ton référentiel est maintenant compatible avec tes scans.")

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    maj_referentiel()
