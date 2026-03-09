import sys
import platform
import os


def get_platform():
    """Detect the current operating system"""
    return platform.system()

def main():
    """Main function to choose between Windows and Linux diagnostics"""
    print("\n" + "="*60)
    print("     NTL-SysToolbox - DIAGNOSTIQUE SYSTÈME")
    print("="*60 + "\n")
    
    print("Sélectionnez une plateforme:")
    print("1. Windows")
    print("2. Linux")
    print("3. Quitter")
    
    try:
        choice = input("\nFaites votre choix (1, 2 ou 3): ").strip()
        
        if choice == "1":
            print("\n--- Diagnostique Windows ---\n")
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from Diags.platform_windows import display_system_info, get_system_info
            display_system_info()
            return get_system_info()
            
        elif choice == "2":
            print("\n--- Diagnostique Linux ---\n")
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from Diags.platform_linux import display_system_info, get_system_info
            display_system_info()
            return get_system_info()
            
        elif choice == "3":
            print("\nAu revoir!")
            sys.exit(0)
            
        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")
            main()
            
    except KeyboardInterrupt:
        print("\n\nProgramme interrompu par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()