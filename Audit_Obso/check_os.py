import nmap
import winrm
import paramiko
import warnings
import getpass
import csv
import sys

warnings.filterwarnings("ignore")

def get_os_via_ssh(ip, user, pwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=user, password=pwd, timeout=2, auth_timeout=2)
        stdin, stdout, stderr = client.exec_command("cat /etc/os-release | grep PRETTY_NAME | cut -d'\"' -f2")
        result = stdout.read().decode().strip()
        client.close()
        return result if result else "Linux"
    except:
        return None

def get_os_via_winrm(ip, user, pwd):
    # AJOUT DE L'ENDPOINT : Sans l'URL complète, WinRM ne sait pas où taper
    endpoint = f'http://{ip}:5985/wsman'

    # On garde ton transport NTLM et ton format d'utilisateur
    session = winrm.Session(
        endpoint,
        auth=(user, pwd),
        transport='ntlm',
        server_cert_validation='ignore',
        read_timeout_sec=5,
        operation_timeout_sec=2
    )

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
        else:
            return None
    except Exception as e:
        # Affiche l'erreur pour comprendre le blocage (ex: credentials rejected)
        print(f"\n[DEBUG {ip}] Erreur WinRM: {e}")
        return None

def scan_os():
    print("--- Audit Obsolescence Optimisé ---")

    u_ssh = input("User SSH (Linux) : ").strip() or "vagrant"
    u_win_raw = input("User WinRM (Windows) : ").strip() or "Administrateur"

    # On conserve ton format obligatoire
    u_win = f"{u_win_raw}@projetamane.epsi"

    mdpwin = getpass.getpass("Mot de passe WinRM : ").strip() or "MotDePasse123"
    mdpssh = getpass.getpass("Mot de passe SSH : ").strip() or "vagrant"
    target = input("Plage IP : ").strip() or "192.168.10.0/24"

    nm = nmap.PortScanner()
    results = []

    try:
        print(f"\n[+] Scan rapide (Ping) sur {target}...")
        nm.scan(hosts=target, arguments='-sn')
        hosts_list = nm.all_hosts()

        for host in hosts_list:
            final_os = "Inconnu"
            print(f"[*] Test {host}...", end=" ", flush=True)

            # 1. SSH
            os_ssh = get_os_via_ssh(host, u_ssh, mdpssh)
            if os_ssh:
                final_os = os_ssh
                print(f"[SSH OK]")
            else:
                # 2. WinRM
                os_win = get_os_via_winrm(host, u_win, mdpwin)
                if os_win:
                    final_os = os_win
                    print(f"[WinRM OK]")
                else:
                    print(f"[ÉCHEC]")

            results.append([host, final_os])

        with open("inventaire_os.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["IP", "OS"])
            writer.writerows(results)

        print(f"\n[OK] Terminé.")

    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    scan_os()
