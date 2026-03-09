import platform
import psutil
from datetime import datetime

def get_os_version():
    """Get Linux OS version"""
    return platform.platform()

def get_uptime():
    """Get system uptime"""
    try:
        # Calculer l'uptime à partir du boot time
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        return str(uptime).split('.')[0]  # Enlever les microsecondes
    except Exception as e:
        return f"Erreur: {e}"

def get_cpu_usage():
    """Get CPU usage percentage"""
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    """Get RAM usage"""
    ram = psutil.virtual_memory()
    return {
        'total': ram.total / (1024**3),
        'used': ram.used / (1024**3),
        'available': ram.available / (1024**3),
        'percent': ram.percent
    }

def get_disk_usage():
    """Get disk usage for all partitions"""
    disks = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks[partition.mountpoint] = {
                'total': usage.total / (1024**3),
                'used': usage.used / (1024**3),
                'free': usage.free / (1024**3),
                'percent': usage.percent
            }
        except PermissionError:
            pass
    return disks

def display_system_info():
    """Display all system information in a formatted way"""
    print("\n" + "="*60)
    print("          DIAGNOSTIQUE DU SYSTÈME LINUX")
    print("="*60 + "\n")
    
    # OS Version
    print(" VERSION DU SYSTÈME D'EXPLOITATION:")
    print(f"   {get_os_version()}\n")
    
    # Uptime
    print("  UPTIME DU SYSTÈME:")
    print(f"   {get_uptime()}\n")
    
    # CPU Usage
    print(" UTILISATION CPU:")
    cpu_percent = get_cpu_usage()
    print(f"   {cpu_percent}%\n")
    
    # RAM Usage
    print(" UTILISATION MÉMOIRE (RAM):")
    ram = get_ram_usage()
    print(f"   Total:      {ram['total']:.2f} GB")
    print(f"   Utilisée:   {ram['used']:.2f} GB")
    print(f"   Disponible: {ram['available']:.2f} GB")
    print(f"   Pourcentage: {ram['percent']}%\n")
    
    # Disk Usage
    print(" UTILISATION DISQUE:")
    disks = get_disk_usage()
    if disks:
        for mountpoint, usage in disks.items():
            print(f"   {mountpoint}:")
            print(f"      Total:      {usage['total']:.2f} GB")
            print(f"      Utilisé:    {usage['used']:.2f} GB")
            print(f"      Libre:      {usage['free']:.2f} GB")
            print(f"      Pourcentage: {usage['percent']}%")
    else:
        print("   Aucun disque détecté")
    
    print("\n" + "="*60 + "\n")

def get_system_info():
    """Get all system information"""
    return {
        'os_version': get_os_version(),
        'uptime': get_uptime(),
        'cpu_percent': get_cpu_usage(),
        'ram': get_ram_usage(),
        'disks': get_disk_usage()
    }

# Afficher les informations au démarrage du module
if __name__ == "__main__":
    display_system_info()