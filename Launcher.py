import os, sys, subprocess, json
from datetime import datetime

class CLIInterface:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.menu_options = {
            1: ("Diagnostics Systèmes", "Diagnostics/diag_system.py"),
            2: ("Sauvegardes WMS", "Sauv_wms/wms_save.py"),
            3: ("Audit d'Obsolescence", "Audit_Obso/audit_obso.py")
        }

    def display_menu(self):
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        print("\n" + "="*60)
        print("          NTL-SysToolbox - Menu Principal")
        print("="*60 + "\n")
        for k, (t, _) in self.menu_options.items():
            print(f"  {k}. {t}")
        print("\n  0. Quitter\n" + "="*60)

    def run_script(self, path, title):
        script_path = os.path.join(self.base_dir, path)
        if not os.path.exists(script_path):
            print(f"Erreur : Fichier introuvable")
            return

        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        try:
            print(f"\n>>> Lancement de : {title}")
            print("-" * 30)

            p = subprocess.Popen(
                [sys.executable, "-u", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                bufsize=0
            )

            out = ""
            while True:
                char = p.stdout.read(1)
                if not char and p.poll() is not None:
                    break
                if char:
                    print(char, end="", flush=True)
                    out += char

            code = p.wait()
            self.logjson(title, code, out)

            print("-" * 30)
            print(">>> Retour au Menu Principal.")

        except KeyboardInterrupt:
            print("Interruption du script.")
        except Exception as e:
            print(f"Erreur lors du lancement : {e}")

    def logjson(self, name, code, output):
        dossier = os.path.join(self.base_dir, "logs")
        os.makedirs(dossier, exist_ok=True)

        # Détection d'erreur dans le texte pour le status
        status = "OK"
        if code != 0 or "[!]" in output or "[ERREUR]" in output:
            status = "ERROR"

        ts = datetime.now()
        data = {
            "timestamp": ts.isoformat(),
            "module": name,
            "exit_code": code,
            "status": status,
            "details": output.splitlines()
        }

        fichier = f"log_{name.replace(' ','_')}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(dossier, fichier), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n[INFO] logs/{fichier}")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Sélectionnez une option : ").strip()

            if choice == "0":
                print("\n Au revoir !")
                break

            if not choice.isdigit() or int(choice) not in self.menu_options:
                print("\n [!] Choix non valide."); continue

            t, p = self.menu_options[int(choice)]
            try:
                self.run_script(p, t)
                input("\nAppuyez sur Entrée pour continuer...")
            except KeyboardInterrupt:
                sys.exit(0)

if __name__ == "__main__":
    CLIInterface().run()
