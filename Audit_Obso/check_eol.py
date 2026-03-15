import pandas
import requests
from datetime import datetime
import time
import os
import re


def get_eol_data(product):
    url = f"https://endoflife.date/api/{product.lower()}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def clean_os_info(raw_os):
    raw_os = raw_os.lower()
    product = "inconnu"
    version = "inconnu"

    if "windows server" in raw_os:
        product = "windows-server"
        match = re.search(r'(2008|2012|2016|2019|2022)', raw_os)
        if match:
            version = match.group(1)

    elif "windows" in raw_os:
        product = "windows"
        major = re.search(r'(10|11)', raw_os)
        v_h2 = re.search(r'(\d{2}h\d)', raw_os)

        if major and v_h2:
            version = f"{major.group(1)}-{v_h2.group(1)}"
        elif major:
            version = major.group(1)

    elif "ubuntu" in raw_os:
        product = "ubuntu"
        match = re.search(r'(\d{2}\.\d{2})', raw_os)
        if match:
            version = match.group(1)

    elif "debian" in raw_os:
        product = "debian"
        match = re.search(r'(\d+)', raw_os)
        if match:
            version = match.group(1)

    return product, version


def run_eol_audit(input_file="inventaire_os.csv"):

    if not os.path.exists(input_file):
        print(f"Erreur : {input_file} introuvable.")
        return

    dataframe = pandas.read_csv(input_file)

    audit_results = []
    cache_api = {}

    for _, row in dataframe.iterrows():

        ip = row["IP"]
        raw_os = str(row["OS"])

        product, version = clean_os_info(raw_os)

        statut = "Inconnu"

        if product != "inconnu" and version != "inconnu":

            if product not in cache_api:
                cache_api[product] = get_eol_data(product)
                time.sleep(0.5)

            data = cache_api[product]

            if data:

                cycle_info = next(
                    (item for item in data if str(item["cycle"]).lower() == version.lower()),
                    None
                )

                if cycle_info:

                    eol_raw = cycle_info.get("eol")

                    if eol_raw is False:
                        statut = "Supporte"

                    elif eol_raw is True:
                        statut = "Obsolete"

                    else:
                        try:
                            eol_dt = datetime.strptime(str(eol_raw), "%Y-%m-%d")
                            today = datetime.now()

                            if eol_dt < today:
                                statut = "Obsolete"
                            elif (eol_dt - today).days < 180:
                                statut = "Bientot obsolete"
                            else:
                                statut = "Supporte"

                        except:
                            statut = "Supporte"

                else:

                    if "-" in version:
                        short_version = version.split("-")[1]

                        cycle_info = next(
                            (item for item in data if str(item["cycle"]).lower() == short_version),
                            None
                        )

                        if cycle_info:
                            statut = "Supporte"
                        else:
                            statut = "Version inconnue"

        audit_results.append({
            "IP": ip,
            "OS": raw_os,
            "Statut": statut
        })

    report_dataframe = pandas.DataFrame(audit_results)

    # dossier des rapports
    dossier = "rapport_os"
    os.makedirs(dossier, exist_ok=True)

    # nom du rapport avec date
    date_du_jour = datetime.now().strftime("%Y-%m-%d")
    chemin_fichier = os.path.join(dossier, f"rapport_os_{date_du_jour}.csv")

    report_dataframe.to_csv(chemin_fichier, index=False, encoding="utf-8")

    print(f"Rapport genere : {chemin_fichier}")


if __name__ == "__main__":
    run_eol_audit()
