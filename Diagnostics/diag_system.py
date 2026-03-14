import sys
import platform
import os

def main():
    """Fonction principale du diagnostic"""
    # On clear pour une lecture plus compréhensive
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\n" + "="*60)
    print("      NTL-SysToolbox - DIAGNOSTIQUE SYSTÈME")
    print("="*60 + "\n")

    print("Sélectionnez une plateforme:")
    print("1. Windows")
    print("2. Linux")
    print("3. Check AD/DNS")
    print("4. Check MySQL")
    print("5. Retour au menu principal")

    try:
        choice = input("\nFaites votre choix (1, 2, 3, 4 ou 5): ").strip()

        # trouver le dossier 'Diags'
        # grâce au subprocess, __file__ est correctement défini
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)

        if choice == "1":
            print("\n--- Diagnostique Windows ---\n")
            from Diags.platform_windows import display_system_info
            display_system_info()

        elif choice == "2":
            print("\n--- Diagnostique Linux ---\n")
            from Diags.platform_linux import display_system_info
            display_system_info()
            
        elif choice == "3":
            print("\n--- Diagnostique AD/DNS ---\n")
            from Diags.check_ad import executer_diagnostic
            executer_diagnostic()
            
        elif choice == "4":
            print("\n--- Diagnostique AD/DNS ---\n")
            from Diags.check_mysql import test_mysql_connection
            test_mysql_connection()
            
        elif choice == "5":
            print("\nRetour...")
            return # Retourne au menu principal

        else:
            print("Choix invalide.")
            main() # Relance le menu de Diags si mauvais choix

    except KeyboardInterrupt:
            # Si on fait Ctrl+C pendant que le script tourne
        print("\n\n [!] Interruption par l'utilisateur (Ctrl+C).")
    except Exception as e:
        print(f"\n[X] Erreur dans le script de diagnostic : {e}")

# Sans ces deux lignes, subprocess ne lancera rien
if __name__ == "__main__":
    main()
