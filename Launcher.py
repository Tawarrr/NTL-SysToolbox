import os
import sys
import subprocess

class CLIInterface:
    def __init__(self):
        # Répertoire de base où se trouve le Launcher.py
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Menu statique référencant les Modules
        self.menu_options = {
            1: {"title": "Diagnostics Systèmes", "path": "Diagnostics/diag_system.py"},
            2: {"title": "Sauvegardes WMS",      "path": "Sauv_wms/wms_save.py"},
            3: {"title": "Audit d'Obsolescence", "path": "Audit_Obso/audit_obso.py"}
        }

    def display_menu(self):
        # Clear l'écran pour meilleure visibilité
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*60)
        print("          NTL-SysToolbox - Menu Principal")
        print("="*60 + "\n")

        for key, info in self.menu_options.items():
            print(f"  {key}. {info['title']}")

        print(f"\n  0. Quitter")
        print("\n" + "="*60)

    def run_script(self, relative_path, title):
        # Construction du chemin absolu du fichier .py à lancer
        script_path = os.path.abspath(os.path.join(self.base_dir, relative_path))

        if not os.path.exists(script_path):
            print(f"\n [!] Erreur : Fichier introuvable à :\n {script_path}")
            return

        try:
            print(f"\n>>> Lancement de : {title}")
            print("-" * 30)

            # Utilisation de subprocess
            subprocess.run([sys.executable, script_path], check=False)

            print("-" * 30)
            print(">>> Retour au Menu Principal.")
        except KeyboardInterrupt:
            print("\n\n [!] Interruption du script.")
        except Exception as e:
            print(f"\n [X] Erreur lors du lancement : {e}")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Sélectionnez une option : ").strip()

            if choice == "0":
                print("\n Au revoir !")
                break

            try:
                c_int = int(choice)
                if c_int in self.menu_options:
                    opt = self.menu_options[c_int]
                    self.run_script(opt['path'], opt['title'])
                    input("\nAppuyez sur Entrée pour continuer...")
                else:
                    print("\n [!] Choix non valide.")
                    input("Appuyez sur Entrée...")
            except ValueError:
                print("\n [!] Veuillez entrer un chiffre.")
                input("Appuyez sur Entrée...")
            except KeyboardInterrupt:
                print("\n\n [!] Programme quitté proprement.")
                sys.exit(0)
if __name__ == "__main__":
    try:
        cli = CLIInterface()
        cli.run()
    except KeyboardInterrupt:
        sys.exit(0)
