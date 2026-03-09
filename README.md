# 🧰 NTL-SysToolbox

⚡ CLI Python pour regrouper des actions d’exploitation (diagnostic, backup, audit) et sortir des résultats clairs + des rapports (JSON/CSV) réutilisables.

##    Ce que ça fait   ##

- 🩺 **Diagnostic** : checks réseau/services (DNS, ports, endpoints, etc.)
- 💾 **Backup** : sauvegardes horodatées vers un répertoire cible
- 🧾 **Audit** : collecte d’infos + export pour reporting

## 🛠️ Installation
📌 Pré-requis : Python 3.10+

```bash
git clone https://github.com/Tawarrr/NTL-SysToolbox.git
cd NTL-SysToolbox
python -m venv .venv
```
# Linux
### Installer venv : apt install python3-venv -y
### Installer pip : apt install pip -y
```bash
source .venv/bin/activate
```
# Windows (PowerShell)
### Installer venv
### Installer pip

```powershell
`.\.venv\Scripts\Activate.ps1`
```

### Sur Windows
```powershell
pip install -r requirements.txt
```

### Sur Linux : `nano requirements.txt` (modules python à installer)
```bash
pip install -r requirements.txt
```

### Sur les deux
```bash
pip install -U pip
pip install -e .
```
