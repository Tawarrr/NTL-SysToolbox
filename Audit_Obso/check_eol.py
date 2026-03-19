import mysql.connector
import requests
import time

def get_eol_data(product):
    url = f"https://endoflife.date/api/{product.lower()}.json"
    try:
        r = requests.get(url, timeout=10)
        return r.json() if r.ok else None
    except Exception as e:
        print(f"  [!] Erreur API pour {product}: {e}")
        return None

def eol_dates():
    print("--- Audit des dates de fin de vie (EOL) ---")

    db = mysql.connector.connect(
        host='192.168.10.21',
        user='admin',
        password='PASSWORD',
        database='EOL_DB'
    )
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT version.id, version.version, os.nom as product_name
        FROM version
        JOIN os ON version.os_id = os.id
        WHERE version.date_eol IS NULL AND os.nom != 'Inconnu'
    """)
    versions_to_check = cursor.fetchall()

    if not versions_to_check:
        print("[*] Aucune nouvelle version à auditer.")
        return

    cache_api = {}

    for row in versions_to_check:
        v_id = row['id']
        cycle = str(row['version']).lower()
        product = row['product_name']
        api_product = 'ubuntu' if product == 'linux' else product

        print(f"[*] Vérification de {api_product} cycle {cycle}...", end=" ")

        if api_product not in cache_api:
            cache_api[api_product] = get_eol_data(api_product)
            time.sleep(0.5)

        data = cache_api[api_product]
        found_date = next(
            (e.get('eol') for e in data or [] if str(e['cycle']).lower() == cycle),
            None
        )

        if found_date:
            cursor.execute(
                "UPDATE version SET date_eol = %s WHERE id = %s",
                (found_date, v_id)
            )
            print(f"[OK] {found_date}")
        else:
            print("[ABSENT]")

    db.commit()
    db.close()
    print("\n[OK] Mise à jour des dates EOL terminée.")

if __name__ == "__main__":
    eol_dates()
