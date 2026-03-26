# NTL-SysToolbox

Outil Python permettant de lancer au choix 1 des 3 modules codés (Diagnostic, Backup/Export, Audit d'obsolescence) et sortir des résultats en fin de script.

## Ce que ça fait ##

- **Diagnostic** : Check ressources des serveurs, services AD/DNS, MySQL
- **Backup** : sauvegardes horodatées vers un répertoire cible (Table ou Base complète)
- **Audit** : collecte d’infos + export pour reporting

##Installation
Pré-requis : Python3 minimum

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


# Test de l'outil avec une infra type

## Vagrant

Dans ce projet, nous avons mis en place une infrastructure automatisée avec Vagrant et Ansible, permettant de pouvoir tester notre outil.

## Utilisation

Pour utiliser cet outil, il faut décompresser le **`Vagrant.zip`** fourni dans le repo, à la suite de ça, un README.md est fourni dedans. Pour utiliser cette infrasrtucture, l'hyperviseur à utiliser est VMware Workstation Pro 25H2 minimum.

### Installation Vagrant : 

#### `installer vagrant` via leur site officiel 

https://developer.hashicorp.com/vagrant/install

Laisser l'installation se faire, redémarrer le poste

ensuite ouvrir un cmd et lancer cette commande : 
```powershell
vagrant plugin install vagrant-vmware-desktop
```
et juste après lancer le `vagrant-vmware-utility.msi`


Vagrant sera bien installé, et pour lancer le setup des machines en automatique, se rendre dans le dossier avec tous les fichiers comme le Vagrantfile etc, 
`clic-droit --> Ouvrir dans le terminal et taper la commande : `
```powershell
vagrant up
```

Toutes les machines vont s'installer une à une, si vous voulez avoir les vm sur votre VMware

se rendre sur l'appli `VMware Workstation Pro --> Clic droit --> Ouvrir`

se rendre dans le dossier :
`Vagrant --> .vagrant --> machines --> {machine_au_choix} --> vmware_desktop --> {id_machine} --> {machine_au_choix}.vmx`

(les identifiants + Mot de passe sont spécifiés dans le .env du **`Vagrant.zip`**)

