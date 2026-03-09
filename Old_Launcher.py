3#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## Main qui exécute tous les codes des répertoires src, Sauv_wms et aud_obso.
## Compatible Windows et Linux

import os
import sys
import platform

class CLIInterface:
    #Interface CLI pour exécuter les scripts des repertoires src, Sauv_wms et aud_obso#
    
    def __init__(self):
        # Détection automatique du chemin (fonctionne sur clé USB)
        self.base_dir = self.get_base_directory()
        self.src_dir = os.path.join(self.base_dir, "src")
        self.Sauv_wms_dir = os.path.join(self.base_dir, "Sauv_wms")
        self.aud_obso_dir = os.path.join(self.base_dir, "aud_obso")
        self.scripts = {}
        self.scripts.update(self.discover_scripts(self.Sauv_wms_dir))
        self.scripts.update(self.discover_scripts(self.aud_obso_dir))
        self.scripts.update(self.discover_scripts(self.src_dir))
        

    def get_base_directory(self):
        #Retourne le répertoire de base du projet (là où se trouve 1NTL-Stlb.py)#
            return os.path.dirname(os.path.abspath(__file__))
            
    
    def discover_scripts(self, src_dir):
        #Découvre tous les scripts Python exécutables dans le répertoire src#
        scripts = {}
        excluded = ['1NTL-Stlb.py', '__init__.py', 'setup.py']
        idx = 1

    def discover_scripts(self, Sauv_wms_dir):
        #Découvre tous les scripts Python exécutables dans le répertoire sauv_wms#
        scripts = {}
        excluded = ['1NTL-Stlb.py', '__init__.py', 'setup.py']
        idx = 1

    def discover_scripts(self, aud_obso_dir):
        #Découvre tous les scripts Python exécutables dans le répertoire aud_obso#
        scripts = {}
        excluded = ['1NTL-Stlb.py', '__init__.py', 'setup.py']
        idx = 1
        
    
        
        # Vérifier que le répertoire source existe
        if not os.path.exists(self.src_dir):
            print(f"  Répertoire introuvable: {self.src_dir}")
            # Tentative avec chemin relatif
            self.src_dir = os.path.join(os.getcwd(), "src")
            if not os.path.exists(self.src_dir):
                print(f"  Répertoire introuvable: {self.src_dir}")
                return scripts  
                
        if not os.path.exists(self.Sauv_wms_dir):
            print(f"  Répertoire introuvable: {self.Sauv_wms_dir}")    
        self.Sauv_wms_dir = os.path.join(os.getcwd(), "Sauv_wms")             
        if not os.path.exists(self.Sauv_wms_dir):
            print(f"  Répertoire introuvable: {self.Sauv_wms_dir}")
            return scripts
        
        if not os.path.exists(self.aud_obso_dir):
            print(f"  Répertoire introuvable: {self.aud_obso_dir}")
        self.aud_obso_dir = os.path.join(os.getcwd(), "aud_obso")
        if not os.path.exists(self.aud_obso_dir):
            print(f"  Répertoire introuvable: {self.aud_obso_dir}")
            return scripts
        
        print(f"  Scan du répertoire: {self.src_dir}")
        print (f" Scan du répertoire: {self.Sauv_wms_dir}")
        print (f" Scan du répertoire: {self.aud_obso_dir}")

        # Scanner tous les fichiers .py
        try:
            for filename in sorted(os.listdir(self.src_dir)):
                if filename.endswith('.py') and filename not in excluded:
                    filepath = os.path.join(self.src_dir, filename)
                    script_name = filename[:-3]  # Enlever .py

                    if os.path.isfile(filepath):
                     scripts[idx] = {
                            'name': script_name,
                            'file': filename,
                            'path': filepath,
                            'type': 'file'
                        }
            idx += 1

            for filename in sorted(os.listdir(self.Sauv_wms_dir)):
             if filename.endswith('.py') and filename not in excluded:
                filepath = os.path.join(self.Sauv_wms_dir, filename)
                script_name = filename[:-3]
                if os.path.isfile(filepath):
                    scripts[idx] = {
                        'name': script_name,
                        'file': filename,
                        'path': filepath,
                        'type': 'file'
                    }
                idx += 2
                
            for filename in sorted(os.listdir(self.aud_obso_dir)):
             if filename.endswith('.py') and filename not in excluded:
                filepath = os.path.join(self.aud_obso_dir, filename)
                script_name = filename[:-3]

                if os.path.isfile(filepath):
                    scripts[idx] = {
                        'name': script_name,
                        'file': filename,
                        'path': filepath,
                        'type': 'file'
                    }
                idx += 3
                
            # Vérifier que c'est un fichier (pas un dossier)
            
        except PermissionError:
            print(" Erreur de permission lors du scan du répertoire")
        except Exception as e:
            print(f" Erreur lors du scan: {e}")
        
        return scripts
    
    def display_menu(self):
        #Affiche le menu principal#
        # Commande clear multiplateforme
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "="*60)
        print("     NTL-SysToolbox - Menu Principal")
        print("="*60 + "\n")
        
        # Informations sur les répertoires
    
        print(f"  Répertoire source: {self.src_dir}")
        print(f"  Répertoire Sauv_wms: {self.Sauv_wms_dir}")
        print(f"  Répertoire aud_obso: {self.aud_obso_dir}")

        print("\n  -----Outils disponibles:-----\n")
        
        if not self.scripts:
            print("  Aucun Outil trouvé.")
            print("  Vérifiez que les dossiers des outils existent et contient des fichiers .py")
        else:
            for idx, script in self.scripts.items():
                print(f"  {idx}. {script['name']}")
        
        print(f"\n  0. Quitter")
        print("\n" + "="*60)
    
    def run_script(self, script_path, script_name):
        #Exécute un script Python directement dans le même processus#
        try:
            print(f"\n Exécution du script: {script_name}\n")
            print("-"*60 + "\n")
            
            # Ajouter les chemins nécessaires pour les imports
            if self.src_dir not in sys.path:
                sys.path.insert(0, self.src_dir)
            
            if self.Sauv_wms_dir not in sys.path:
                sys.path.insert(0, self.Sauv_wms_dir)

            if self.aud_obso_dir not in sys.path:
                sys.path.insert(0, self.aud_obso_dir)

            # Ajouter le dossier Diags s'il existe
            diags_dir = os.path.join(self.src_dir, "Diags")
            if os.path.exists(diags_dir) and diags_dir not in sys.path:
                sys.path.insert(0, diags_dir)

            Sauv_dir = os.path.join(self.Sauv_wms_dir, "sauv_bdd")
            if os.path.exists(Sauv_dir) and Sauv_dir not in sys.path:
                sys.path.insert(0, Sauv_dir)
        
            Sauv_dir = os.path.join(self.Sauv_wms_dir, "sauv_tab")
            if os.path.exists(Sauv_dir) and Sauv_dir not in sys.path:
                sys.path.insert(0, Sauv_dir)

            aud_obso_dir = os.path.join(self.aud_obso_dir, "aud_obso")
            if os.path.exists(aud_obso_dir) and aud_obso_dir not in sys.path:
                sys.path.insert(0, aud_obso_dir)
            
            # Lire et exécuter le script
            with open(script_path, 'r', encoding='utf-8') as f:
                script_code = f.read()
            
            # Créer un namespace avec les modules nécessaires
            namespace = {
                '__name__': '__main__',
                '__file__': script_path,
                'os': os,
                'sys': sys,
                'platform': platform
            }
            
            # Exécuter le script
            exec(script_code, namespace)
            
            print("\n" + "-"*60)
            print("\n Outil exécuté avec succès!\n")
            
        except Exception as e:
            print(f"\n Erreur lors de l'exécution: {e}\n")
            import traceback
            traceback.print_exc()
    
    def run(self):
        #Boucle principale#
        while True:
            self.display_menu()
            
            try:
                choice = input("Sélectionnez une option: ").strip()
                
                if choice == "0":
                    print("\n Au revoir!\n")
                    sys.exit(0)
                
                choice_int = int(choice)
                
                if choice_int in self.scripts:
                    script = self.scripts[choice_int]
                    self.run_script(script['path'], script['name'])
                    input("\nAppuyez sur Entrée pour continuer...")



                else:
                    print("\n Choix invalide. Veuillez réessayer.\n")
                    input("Appuyez sur Entrée pour continuer...")
                    
            except ValueError:
                print("\n Veuillez entrer un nombre valide.\n")
                input("Appuyez sur Entrée pour continuer...")
            except KeyboardInterrupt:
                print("\n\n Programme interrompu par l'utilisateur.")
                sys.exit(0)
            except Exception as e:
                print(f"\n Erreur: {e}\n")
                input("Appuyez sur Entrée pour continuer...")

def main():
    #Fonction principale#
    print("=== NTL-SysToolbox Luncher ===\n")
    
    # Vérification de psutil (optionnel)
    try:
        import psutil
    except ImportError:
        print("  Bibliothèque 'psutil' non installée.")
        print("   Certains scripts peuvent ne pas fonctionner.")
        print("   Lancez 'setup.py' pour l'installer.\n")
        input("Appuyez sur Entrée pour continuer...")
    
    cli = CLIInterface()
    
    
    # a refaire une fois le projet structuré complet
    if not cli.scripts:
        print(f"\n Aucun script trouvé dans: {cli.src_dir}")
        print(f"\n Aucun script trouvé dans: {cli.Sauv_wms_dir}")
        print(f"\n Aucun script trouvé dans: {cli.aud_obso_dir}")
        print("\n Structure attendue:")
        print("    NTL-SysToolbox/")
        print("   ├── 1NTL-Stlb.py  (ce script)")
        print("   ├── Sauv_wms/")
        print("   │   ├── Sauvs.py")# rajouter les chemins module 2
        print("   │   ├── sauv_bdd/ ")
        print("   │   |   ├── sauv_bdd.py/")
        print("   │   └── sauv_tab/")
        print("   │       └── sauv_tab.py/")
        print("   ├── aud_obso/") # rajouter les chemins module 3
        print("   └──  src/")# rajouter les chemins module 1
        print("       ├── diagnostic.py")
        print("       ├── setup.py")
        print("       └──  Diags/")
        print("           ├── platform_windows.py")
        print("           └── platform_linux.py")
        sys.exit(1)
    
    cli.run()

if __name__ == "__main__":
    main()