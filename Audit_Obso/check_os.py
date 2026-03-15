import nmap
import winrm
import warnings
import getpass
import csv

warnings.filterwarnings("ignore")

def get_os_via_winrm(ip, user, pwd):
    session = winrm.Session(ip, auth=(user, pwd), transport='ntlm', server_cert_validation='ignore')
    ps_cmd = """
    $info = Get-ItemProperty "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion"
    $name = $info.ProductName
    $ver = $info.DisplayVersion
    if ($ver) { "$name ($ver)" } else { "$name" }
    """
    try:
        r = session.run_ps(ps_cmd)
        if r.status_code == 0:
            return r.std_out.decode('latin-1', errors='ignore').strip()
    except:
        pass
    return None

def scan_os():
    print("--- Audit Obsolescence : Scan & Export CSV ---")

    admin = input("Administrateur du domaine : ").strip() or "Administrateur"
    mdpadmin = getpass.getpass(f"Mot de passe de l'admin du domaine : ")
    adminfqdn = f"{admin}@projetamane.epsi"
    target = input("Plage IP : ").strip() or "192.168.10.0/24"

    nm = nmap.PortScanner()
    results = []

    try:
        print(f"\n[+] Scan en cours...")
        nm.scan(hosts=target, arguments='-Pn -sV -O --osscan-guess -T4')

        for host in nm.all_hosts():
            final_os = "Inconnu"

            # Pour Linux
            banner_info = ""
            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    svc = nm[host][proto][port]
                    banner_info += f" {svc.get('product', '')} {svc.get('version', '')}"

            if "ubuntu" in banner_info.lower():
                if "7.6p1" in banner_info: final_os = "Ubuntu 18.04"
                elif "8.2p1" in banner_info: final_os = "Ubuntu 20.04"
                elif "8.9p1" in banner_info: final_os = "Ubuntu 22.04"
                elif "9.6p1" in banner_info: final_os = "Ubuntu 24.04"
                else: final_os = "Ubuntu"
            elif "debian" in banner_info.lower():
                if "deb10" in banner_info: final_os = "Debian 10"
                elif "deb11" in banner_info: final_os = "Debian 11"
                elif "deb12" in banner_info: final_os = "Debian 12"
                else: final_os = "Debian"

            # Pour Windows
            if final_os == "Inconnu":
                win_os = get_os_via_winrm(host, adminfqdn, mdpadmin)
                if win_os:
                    final_os = win_os
                else:
                    if 'osmatch' in nm[host] and len(nm[host]['osmatch']) > 0:
                        final_os = nm[host]['osmatch'][0]['name']

            results.append([host, final_os])
            print(f"{host:<15} | {final_os}")

        # Fichier CSV
        filename = "inventaire_os.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["IP", "OS"]) # Header
            writer.writerows(results)

        print(f"\n[OK] Fichier '{filename}' généré avec succès.")

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    scan_os()
