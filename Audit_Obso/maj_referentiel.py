import mysql.connector, os, requests
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_MDP')
database = os.getenv('DB_NAME')

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
                    v_majeure = str(entry.get('cycle', ''))
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
                return True
        db.close()
        print("\n[SUCCÈS] Le référentiel EOL est à jour.")
        return True
    except Exception as e:
        print(f"Erreur : {e}")
        return False
if __name__ == "__main__":
    maj_referentiel()
