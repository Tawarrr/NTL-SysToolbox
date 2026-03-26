import socket, subprocess, platform, sys, os

# --- CONFIGURATION ---
try:
    target_ip = input("Entrer l'IP du DC : ").strip()
    target_domain = input("Entrer le domaine : ").strip()
except KeyboardInterrupt:
    sys.exit(1)

def check_service_by_port(ip, port, name):
    """ Vérifie si un port répond et retourne True (OK) ou False (Erreur) """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip, port))
    sock.close()
    
    if result == 0:
        print(f"[OK] Service {name} (Port {port}) : ACTIF")
        return True
    else:
        print(f"[ERREUR] Service {name} (Port {port}) : INACCESSIBLE / ARRÊTÉ")
        return False

def test_dns(domain, server):
    """ Teste la résolution DNS et retourne True ou False """
    try:
        cmd = ["nslookup", domain, server]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

        if result.returncode == 0 and ("Address" in result.stdout or "Addresses" in result.stdout):
            print(f"  [OK] Le DNS répond bien pour '{domain}' via {server}")
            return True
        else:
            print(f"  [ERREUR] Le DNS ne résout pas le domaine '{domain}'")
            return False
    except Exception as e:
        print(f"  [ERREUR] lors du test DNS : {e}")
        return False

def executer_diagnostic():
    """ Lance la suite de tests et compile le résultat final """
    print(f"\n=== DIAGNOSTIC AD & DNS ({platform.system().upper()}) : {target_ip} ===")
    global_success = True 

    # 1. Test des services AD via ports TCP
    print("\n[ÉTAT DES SERVICES VIA LES PORTS]")
    services = {
        389: "Active Directory (NTDS)",
        53:  "Serveur DNS"
    }

    for port, name in services.items():
        if not check_service_by_port(target_ip, port, name):
            global_success = False

    # 2. Test de résolution DNS
    print("\n[VÉRIFICATION REGISTRES DNS]")
    if not test_dns(target_domain, target_ip):
        global_success = False

    print("\n=== FIN DU DIAGNOSTIC ===")
    return global_success

# --- BLOC DE LANCEMENT ---
if __name__ == "__main__":
    diagnostic_reussi = executer_diagnostic()
    print("\n" + "-"*30)
    if not diagnostic_reussi:
        sys.exit(1)
    else:
        sys.exit(0)
