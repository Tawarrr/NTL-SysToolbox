# 🧰 NTL-SysToolbox

⚡ Outil Python permettant de lancer au choix 1 des 3 modules codés (Diagnostic, Backup/Export, Audit d'obsolescence) et sortir des résultats en fin de script.

##    Ce que ça fait   ##

- 🩺 **Diagnostic** : Check ressources des serveurs, services AD/DNS, MySQL
- 💾 **Backup** : sauvegardes horodatées vers un répertoire cible (Table ou Base complète)
- 🧾 **Audit** : collecte d’infos + export pour reporting

## 🛠️ Installation
📌 Pré-requis : Python3 minimum

```bash
git clone https://github.com/Tawarrr/NTL-SysToolbox.git
cd NTL-SysToolbox
```
# Sur Linux
#### Installer venv : apt install python3-venv -y
#### Installer pip : apt install pip -y
```bash
python3 -m venv .venv
source .venv/bin/activate
```
#### Installer les dépendances avec le fichier `requirements.txt`
```bash
pip install -r requirements.txt
```


# Sur Windows (PowerShell)
#### Installer venv (installé de base avec python sur Windows)
#### Installer pip (installé de base avec python sur Windows)

```powershell
py -m venv .venv
**.\.venv\Scripts\Activate.ps1**
```
#### Installer les dépendances avec le fichier `requirements.txt`
```powershell
pip install -r requirements.txt
```

## Pour le bon fonctionnement du script, penser à remplir les variables du .env fourni, permettant les connexions aux machines et à la bdd.


