import sys, platform, os, subprocess
def main():
    """Fonction principale du diagnostic"""
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

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

        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        success = True

        if choice == "1":
            print("\n--- Diagnostique Windows ---\n")
            from Diags.platform_windows import display_system_info
            success = display_system_info()

        elif choice == "2":
            print("\n--- Diagnostique Linux ---\n")
            from Diags.platform_linux import display_system_info
            success = display_system_info()

        elif choice == "3":
            print("\n--- Diagnostique AD/DNS ---\n")
            from Diags.check_ad import executer_diagnostic
            success = executer_diagnostic()

        elif choice == "4":
            print("\n--- Diagnostique MySQL ---\n")
            from Diags.check_mysql import test_mysql_connection
            success = test_mysql_connection()

        elif choice == "5":
            print("\nRetour...")
            return 

        else:
            print("Choix invalide.")
            return main() 

        if success is False:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n [!] Interruption par l'utilisateur (Ctrl+C).")
        sys.exit(1)
    except Exception as e:
        print(f"\n[X] Erreur dans le script de diagnostic : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
