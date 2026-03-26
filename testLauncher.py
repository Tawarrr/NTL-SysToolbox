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
        path = os.path.join(self.base_dir, path)
        if not os.path.exists(path):
            print(f"Fichier {path} introuvable")
            return

        try:
            print(f"{title}" + "-"*30)
            p = subprocess.Popen([sys.executable, path],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 text=True)

            out = []
            for line in p.stdout:
                print(line, end="")
                out.append(line)

            code = p.wait()
            self.logjson(title, code, "".join(out))
            print("-"*30 + "\n>>> Retour menu.")

        except KeyboardInterrupt:
            print("Interruption Ctrl+C. ")
        except Exception as e:
            print(f"\n [X] {e}")

    def logjson(self, name, code, output):
        dossier = os.path.join(self.base_dir, "logs")
        os.makedirs(dossier, exist_ok=True)

        ts = datetime.now()
        data = {
            "timestamp": ts.isoformat(),
            "module": name,
            "exit_code": code,
            "status": "OK" if code == 0 else "ERROR",
            "details": output.splitlines()
        }

        fichier = f"log_{name.replace(' ','_')}_{ts.strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(dossier, fichier), "w", encoding="utf-8") as fileprint:
            json.dump(data, fileprint, indent=4, ensure_ascii=False)

        print(f"\n[INFO] logs/{fichier}")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Choix : ").strip()

            if choice == "0":
                break
            if not choice.isdigit() or int(choice) not in self.menu_options:
                input("\n[!] Invalide..."); continue

            t, p = self.menu_options[int(choice)]
            try:
                self.run_script(p, t)
                input("\nEntrée...")
            except KeyboardInterrupt:
                sys.exit(0)

if __name__ == "__main__":
    CLIInterface().run()
