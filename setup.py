import sys
import subprocess
import platform

def install_psutil():
    #Instalation de la librairie psutil  #
    system = platform.system()
    
    try:
        if system == "Windows":
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
            print("psutil installed successfully on Windows")
        elif system == "Linux":
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
            print("psutil installed successfully on Linux")
        else:
            print(f"Unsupported operating system: {system}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation de psutil: {e}")

def install_pymysql():
    #Instalation de la librairie pymysql#
    system = platform.system()
    
    try:
        if system == "Windows":
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql"])
            print("pymysql a été installé avec succès sur Windows")
        elif system == "Linux":
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql"])
            print("pymysql a été installé avec succès sur Linux")
        else:
            print(f"Unsupported operating system: {system}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation de pymysql: {e}")

if __name__ == "__main__":
    user_choice = input("Do you want to install psutil et pymysql? (yes/no): ").lower()
    
    if user_choice in ["yes", "y"]:
        install_psutil()
        install_pymysql()
    else:
        print("Installation cancelled")


