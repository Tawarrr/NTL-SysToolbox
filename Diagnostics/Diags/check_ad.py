import socket
import subprocess
import platform
import sys

# --- CONFIGURATION ---
target_ip = input("Entrer l'IP du DC : ")      # ex: 192.168.10.10
target_domain = input("Entrer le domaine : ")   # ex: projetama.epsi

def check_service_by_port(ip, port, name):
    """ Vérifie si un port répond sur l'IP cible """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print(f"[OK] Service {name} (Port {port}) : ACTIF")
    else:
        print(f"Service {name} (Port {port}) : INACCESSIBLE / ARRÊTÉ")
    sock.close()

def test_dns(domain, server):
    """ Teste la résolution DNS de manière compatible Linux/Windows """
    try:
        # nslookup est universel
        cmd = ["nslookup", domain, server]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

        if result.returncode == 0 and ("Address" in result.stdout or "Addresses" in result.stdout):
            print(f"  [OK] Le DNS répond bien pour '{domain}' via {server}")
            for line in result.stdout.splitlines():
                if "Address" in line and server not in line:
                    print(f"Détail : Domaine associé au serveur : {server}")
        else:
            print(f"  [!!] Le DNS ne résout pas le domaine '{domain}'")
    except Exception as e:
        print(f"Erreur lors du test DNS : {e}")

def executer_diagnostic():
    """ Lance la suite de tests """
    print(f"\n=== DIAGNOSTIC AD & DNS ({platform.system().upper()}) : {target_ip} ===")

    # 1. Test des services AD via ports TCP
    print("\n[ÉTAT DES SERVICES VIA LES PORTS]")
    services = {
        389: "Active Directory (NTDS)",
        53:  "Serveur DNS"
    }

    for port, name in services.items():
        check_service_by_port(target_ip, port, name)

    # 2. Test de résolution DNS
    print("\n[VÉRIFICATION REGISTRES DNS]")
    test_dns(target_domain, target_ip)

    print("\n=== FIN DU DIAGNOSTIC ===")

# --- BLOC DE LANCEMENT ---
if __name__ == "__main__":
    # On lance le diagnostic quel que soit l'OS
    executer_diagnostic()
    print("\n" + "-"*30)
    input("Appuyez sur Entrée pour fermer cette fenêtre...")
