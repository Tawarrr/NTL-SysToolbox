import nmap, winrm, paramiko, warnings, getpass, mysql.connector, re
warnings.filterwarnings("ignore")

def extraire_regex(pattern, texte):
    match = re.search(pattern, texte)
    return match.group(1) if match else "Inconnu"

def formater_infos_os(os_brut):
    os_minuscule = os_brut.lower()
    if "windows server" in os_minuscule:
        return ("windows-server",
                extraire_regex(r'(2008|2012|2016|2019|2022)', os_minuscule),
                extraire_regex(r'\((.*?)\)', os_minuscule))
    if "ubuntu" in os_minuscule:
        version_majeure = extraire_regex(r'(\d{2}\.\d{2})', os_minuscule)
        return ("linux", version_majeure, extraire_regex(r'(\d{2}\.\d{2}\.\d+)', os_minuscule) or version_majeure)
    return ("Inconnu", "Inconnu", "Inconnu")

def recuperer_os_ssh(adresse_ip, utilisateur, mot_de_passe):
    try:
        client_ssh = paramiko.SSHClient()
        client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client_ssh.connect(adresse_ip, username=utilisateur, password=mot_de_passe, timeout=2, auth_timeout=2)
        flux_sortie = client_ssh.exec_command("grep PRETTY_NAME /etc/os-release")[1].read().decode()
        client_ssh.close()
        return flux_sortie.split("=")[-1].replace('"', '').strip() if flux_sortie else "Linux"
    except: return None

def recuperer_os_winrm(adresse_ip, utilisateur, mot_de_passe):
    try:
        session_winrm = winrm.Session(f'http://{adresse_ip}:5985/wsman', auth=(utilisateur, mot_de_passe), transport='ntlm', server_cert_validation='ignore')
        resultat = session_winrm.run_ps('$i=gp "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion";"$($i.ProductName) ($($i.DisplayVersion))"')
        return resultat.std_out.decode('latin-1').strip() if resultat.status_code == 0 else None
    except: return None

def scan_os():
    print("--- Audit Obsolescence ---")

    user_ssh = input("User SSH : ").strip() or "vagrant"
    user_winrm = (input("User WinRM : ").strip() or "Administrateur") + "@projetamane.epsi"
    pass_winrm = getpass.getpass("Pass WinRM : ").strip() or "MotDePasse123"
    pass_ssh = getpass.getpass("Pass SSH : ").strip() or "vagrant"
    reseau_cible = input("Plage IP : ").strip() or "192.168.10.0/24"

    base_donnees = mysql.connector.connect(host='192.168.10.21', user='admin', password='PASSWORD', database='EOL_DB')
    curseur = base_donnees.cursor()
    curseur.execute("SET time_zone = '+01:00';")

    scanner = nmap.PortScanner()
    scanner.scan(hosts=reseau_cible, arguments='-sn')

    for ip_hote in scanner.all_hosts():
        os_detecte = recuperer_os_ssh(ip_hote, user_ssh, pass_ssh) or recuperer_os_winrm(ip_hote, user_winrm, pass_winrm) or "Inconnu"
        print(f"[*] {ip_hote} : {os_detecte}")

        categorie_os, v_majeure, v_detaillee = formater_infos_os(os_detecte)

        curseur.execute("INSERT IGNORE INTO os (nom_os) VALUES (%s)", (categorie_os,))
        curseur.execute("SELECT id FROM os WHERE nom_os=%s", (categorie_os,))
        id_os = curseur.fetchone()[0]

        curseur.execute("""INSERT INTO version (os_id, ip, version, version_detail, total)
                           VALUES (%s,%s,%s,%s,%s)""",
                        (id_os, ip_hote, v_majeure, v_detaillee, os_detecte))

    base_donnees.commit()
    base_donnees.close()
    print("\n[OK] Terminé")

if __name__ == "__main__":
    scan_os()
