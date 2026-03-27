import nmap, winrm, sys, paramiko, warnings, getpass, mysql.connector, os, re
from dotenv import load_dotenv
load_dotenv()
from maj_referentiel import maj_referentiel
# Ignore les erreurs
warnings.filterwarnings("ignore")

maj = input("Voulez-vous faire une MàJ du référentiel End Of Life de la BDD ? [Y/n] ").strip().lower()

if maj in ('y', 'yes', ''):
    succes_maj = maj_referentiel()
    if succes_maj:
        print("[OK] Référentiel mis à jour avec succès.")
    else:
        print("[!] Échec de la mise à jour du référentiel. Suite du script avec les anciennes données.")
        sys.exit(1)
elif maj in ('n', 'no'):
    print("Mise à jour non effectuée.")
else:
    print("Mauvaise saisie, fin du script.")
    exit()

def extraire_regex(pattern, texte):
    match = re.search(pattern, texte)
    return match.group(1) if match else "Inconnu"

def formater_infos_os(os_brut):
    os_minuscule = os_brut.lower()
    # WS
    if "windows server" in os_minuscule:
        v_majeure = extraire_regex(r'(2008|2012|2016|2019|2022|2025)', os_minuscule)
        # extraction du build
        v_detail = extraire_regex(r'(\d{1,2}\.\d\.\d+)', os_minuscule)
        return ("windows-server", v_majeure, v_detail)

    # Ubuntu
    if "ubuntu" in os_minuscule:
        # version
        v_majeure = extraire_regex(r'(\d{2}\.\d{2})', os_minuscule)
        # latest
        v_detail = extraire_regex(r'(\d{2}\.\d{2}\.\d+)', os_minuscule)
        if v_detail == "Inconnu": v_detail = v_majeure
        return ("linux", v_majeure, v_detail)

    return ("Inconnu", "Inconnu", "Inconnu")

def recuperer_os_ssh(adresse_ip, utilisateur, mot_de_passe):
    try:
        client_ssh = paramiko.SSHClient()
        client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client_ssh.connect(adresse_ip, username=utilisateur, password=mot_de_passe, timeout=3)
        # On récupère le nom complet de l'OS
        stdin, stdout, stderr = client_ssh.exec_command("grep PRETTY_NAME /etc/os-release")
        flux_sortie = stdout.read().decode()
        client_ssh.close()

        if flux_sortie:
            return flux_sortie.split("=")[-1].replace('"', '').strip()
        return "Linux"
    except:
        return None

def recuperer_os_winrm(adresse_ip, utilisateur, mot_de_passe):
    try:
        session_winrm = winrm.Session(
            f'http://{adresse_ip}:5985/wsman',
            auth=(utilisateur, mot_de_passe),
            transport='ntlm',
            server_cert_validation='ignore'
        )

        # PowerShell pour récupérer le nom du produit + le build number (ex: 10.0.20348)
        script_ps = """
        $i = gp "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion";
        $build = "10.0.$($i.CurrentBuildNumber)";
        "$($i.ProductName) ($build)"
        """
        resultat = session_winrm.run_ps(script_ps)
        return resultat.std_out.decode('latin-1').strip() if resultat.status_code == 0 else None
    except:
        return None

def scan_os():
    print("AUDIT INVENTAIRE SERVEURS")

    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_MDP')
    database = os.getenv('DB_NAME')
    user_ssh = os.getenv('SSH_USER')
    user_win = os.getenv('WINRM_USER')
    pass_win = os.getenv('WINRM_MDP')
    pass_ssh = os.getenv('SSH_MDP')
    target   = os.getenv('TARGET')

    # Connexion BDD
    try:
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        curseur = db.cursor()
    except Exception as e:
        print(f"[!] Erreur de connexion BDD : {e}")
        return

    # Scan réseau
    print(f"\n[*] Scan du réseau {target} en cours...")
    nm = nmap.PortScanner()
    nm.scan(hosts=target, arguments='-sn')
    for ip in nm.all_hosts():
        # Détection OS
        os_raw = recuperer_os_ssh(ip, user_ssh, pass_ssh) or \
                 recuperer_os_winrm(ip, user_win, pass_win) or \
                 "Inconnu"

        print(f"[+] {ip.ljust(15)} : {os_raw}")

        # Formatage des données
        cat_os, v_maj, v_det = formater_infos_os(os_raw)
        if cat_os != "Inconnu":
            # Mise à jour table OS
            curseur.execute("INSERT IGNORE INTO os (nom_os) VALUES (%s)", (cat_os,))
            curseur.execute("SELECT id FROM os WHERE nom_os=%s", (cat_os,))
            os_id = curseur.fetchone()[0]

            # Insertion dans table version
            sql_insert = """
                INSERT INTO version (os_id, ip, version, version_detail, total)
                VALUES (%s, %s, %s, %s, %s)
            """
            curseur.execute(sql_insert, (os_id, ip, v_maj, v_det, os_raw))
    db.commit()

    # --- SYNCHRONISATION EOL ---
    # MàJ table versio pour les eol
    print("\n[*] Synchronisation des dates de fin de vie (EOL)...")
    sql_update = """
        UPDATE version
        JOIN os ON version.os_id = os.id
        JOIN referentiel_eol ON os.nom_os = referentiel_eol.nom_os AND version.version = referentiel_eol.version
        SET version.date_eol = referentiel_eol.date_eol
    """
    curseur.execute(sql_update)
    db.commit()

    curseur.close()
    db.close()
    print("[OK] Scan terminé, inscription en BDD.")

if __name__ == "__main__":
    scan_os()
