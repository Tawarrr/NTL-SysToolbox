import sys
import platform
import os

# filepath: g:\MACHINES MSPR\MSPR\NTL-SysToolbox\Sauv_wms\Sauvs.py



def main():
    """Main function to choose between different WMS backup options"""
    print("\n" + "="*60)
    print("     NTL-SysToolbox - Sauvegardes WMS")
    print("="*60 + "\n")
    
    print("Sélectionnez la sauvegarde que vous souhaitez faire:")
    print("1. Sauvegarde Base de données en SQL")
    print("2. Sauvegarde table en CSV")
    print("3. Quitter")
    
    try:
        choice = input("\nFaites votre choix (1, 2 ou 3): ").strip()
        
        if choice == "1":
            print("\n--- Sauvegarde Base de données en SQL ---\n")
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from sauv_bdd.sauv_bdd import connect_to_database 
            return connect_to_database()#ici je met les def qu'il y a dans l'autres fichier sauv_bdd.py 
            
            
        elif choice == "2":
            print("\n--- Sauvegarde table en CSV ---\n")
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from sauv_tab.sauv_tab import save_table_to_CSV 
            return save_table_to_CSV () #ici je met les def qu'il y a dans l'autres fichier sauv_tab.py 
            
            
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