import sys
import os

def main():
    print("\n" + "="*60)
    print("      NTL-SysToolbox - Sauvegardes WMS")
    print("="*60 + "\n")

    print("Sélectionnez la sauvegarde que vous souhaitez faire:")
    print("1. Sauvegarde Base de données en SQL")
    print("2. Sauvegarde table en CSV")
    print("3. Quitter")

    try:
        choice = input("\nFaites votre choix (1, 2 ou 3): ").strip()

        # Construction du chemin pour que Python trouve les sous-dossiers
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)

        if choice == "1":
            print("\n--- Lancement : Sauvegarde SQL ---\n")
            # Importation depuis Sauv_wms/sauv_bdd/sauv_bdd.py
            from sauv_bdd.sauv_bdd import sauvegarder_bdd_sql
            res = sauvegarder_bdd_sql()
            if res is False or res is None:
                sys.exit(1)
            return res

        elif choice == "2":
            print("\n--- Lancement : Sauvegarde CSV ---\n")
            # Importation depuis Sauv_wms/sauv_tab/sauv_tab.py
            from sauv_tab.sauv_tab import save_table_to_CSV
            res = save_table_to_CSV()
            if res is False or res is None:
                sys.exit(1)
            return res

        elif choice == "3":
            return

        else:
            print("Choix invalide.")
            main()

    except Exception as e:
        print(f"Erreur lors de l'appel du module : {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()
