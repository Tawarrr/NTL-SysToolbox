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

# Linux
source .venv/bin/activate

# Windows (PowerShell)
# .\.venv\Scripts\Activate.ps1

pip install -U pip
pip install -e .
