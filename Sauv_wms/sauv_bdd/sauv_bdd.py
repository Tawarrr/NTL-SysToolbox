import os
import sys
from datetime import datetime

# Ajouter le chemin vers ton module de connexion
chemin_connexion = "/media/mspr/USB DISK/NTL-SysToolbox/Sauv_wms/sauv_bdd"
if chemin_connexion not in sys.path:
    sys.path.insert(0, chemin_connexion)

# Importer ta fonction de connexion
# from connex_bdd import connect_to_database
def connect_to_database():
    print("\n--- Connexion MySQL ---")
    host = input("  Hôte / IP  : ").strip() or "WMS-APP"
    user = input("  User [mspr] : ").strip() or "mspr"
    password = getpass.getpass("  Password : ") # mspr
    database = input("  Base [WMS] : ").strip() or "WMS"

    try:
        # Connexion classique sans options de curseur spéciales
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306,
            connect_timeout=10
        )
        print("Connexion OK !\n")
        return conn
    except Exception as e:
        print(f"[ERREUR] : {e}")
        return None
# ============================================
# FONCTION 1 : Créer le dossier backups
# ============================================
def creer_dossier_backup():
    
    #Cree le dossier de sauvegarde s'il n'existe pas
    
    dossier = "/media/mspr/USB DISK/NTL-SysToolbox/Backups_BDD_WMS"
    if not os.path.exists(dossier):
        os.makedirs(dossier)
        print(f"Dossier '{dossier}' cree")
    else:
        print(f"Dossier '{dossier}' existe deja")
    return dossier

# ============================================
# FONCTION 2 : Générer le nom du fichier
# ============================================
def generer_nom_fichier():
    
    #Cree un nom de fichier avec la date et l'heure
    
    maintenant = datetime.now()
    timestamp = maintenant.strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"backup_WMS_{timestamp}.sql"
    return nom_fichier

# ============================================
# FONCTION 3 : Écrire l'en-tête du fichier SQL
# ============================================
def ecrire_entete(fichier, nom_bd):
    
    #Ecrit les commentaires et desactive les contraintes
    
    maintenant = datetime.now()
    date_texte = maintenant.strftime("%Y-%m-%d %H:%M:%S")
    
    fichier.write("-- ===========================================\n")
    fichier.write(f"-- SAUVEGARDE DE LA BASE : {nom_bd}\n")
    fichier.write(f"-- DATE : {date_texte}\n")
    fichier.write("-- ===========================================\n\n")
    fichier.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
    print("  - En-tete ecrit")

# ============================================
# FONCTION 4 : Sauvegarder une table
# ============================================
def sauvegarder_table(fichier, curseur, nom_table):
    
    #Sauvegarde la structure ET les donnees d'une table
    
    print(f"  - Traitement de la table : {nom_table}")
    
    # Structure de la table
    curseur.execute(f"SHOW CREATE TABLE {nom_table}")
    resultat = curseur.fetchone()
    create_table = resultat[1]
    
    fichier.write(f"\n-- Table : {nom_table}\n")
    fichier.write(f"DROP TABLE IF EXISTS `{nom_table}`;\n")
    fichier.write(f"{create_table};\n\n")
    
    # Donnees de la table
    curseur.execute(f"SELECT * FROM {nom_table}")
    donnees = curseur.fetchall()
    
    if donnees:
        # Noms des colonnes
        curseur.execute(f"DESCRIBE {nom_table}")
        colonnes = [col[0] for col in curseur.fetchall()]
        colonnes_texte = ", ".join([f"`{col}`" for col in colonnes])
        
        fichier.write(f"INSERT INTO `{nom_table}` ({colonnes_texte}) VALUES\n")
        
        valeurs_lignes = []
        for ligne in donnees:
            valeurs = []
            for valeur in ligne:
                if valeur is None:
                    valeurs.append("NULL")
                elif isinstance(valeur, (int, float)):
                    valeurs.append(str(valeur))
                else:
                    valeur_texte = str(valeur).replace("'", "\\'")
                    valeurs.append(f"'{valeur_texte}'")
            
            valeurs_lignes.append("(" + ", ".join(valeurs) + ")")
        
        fichier.write(",\n".join(valeurs_lignes))
        fichier.write(";\n")
        print(f"     - {len(donnees)} ligne(s) sauvegardee(s)")
    else:
        fichier.write(f"-- Aucune donnee dans {nom_table}\n")
        print(f"     - Aucune donnee")

# ============================================
# FONCTION PRINCIPALE
# ============================================
def main():
    
    #Fonction principale qui orchestre la sauvegarde
    
    print("\n" + "="*60)
    print("     SAUVEGARDE DE LA BASE WMS")
    print("="*60 + "\n")
    
    # UTILISER TON SCRIPT DE CONNEXION
    print("Utilisation du module de connexion existant...")
    connexion = connect_to_database()
    
    if not connexion:
        print("Impossible de se connecter a la base. Arret de la sauvegarde.")
        return
    
    # Creer le dossier de sauvegarde
    dossier_backup = creer_dossier_backup()
    
    # Generer le nom du fichier
    nom_fichier = generer_nom_fichier()
    chemin_complet = os.path.join(dossier_backup, nom_fichier)
    print(f"Fichier de sortie : {chemin_complet}\n")
    
    try:
        # Ouvrir le fichier en ecriture
        with open(chemin_complet, 'w', encoding='utf-8') as fichier_sql:
            
            # Ecrire l'en-tete
            ecrire_entete(fichier_sql, "WMS")
            
            # Recuperer toutes les tables
            curseur = connexion.cursor()
            curseur.execute("SHOW TABLES")
            tables = curseur.fetchall()
            
            print("Tables trouvees :")
            for table in tables:
                nom_table = table[0]
                sauvegarder_table(fichier_sql, curseur, nom_table)
            
            # Reactiver les cles etrangeres
            fichier_sql.write("\nSET FOREIGN_KEY_CHECKS = 1;\n")
            fichier_sql.write("-- ===========================================\n")
            fichier_sql.write("-- FIN DE LA SAUVEGARDE\n")
            fichier_sql.write("-- ===========================================\n")
        
        # Message de confirmation
        print("\n" + "-"*60)
        print("Sauvegarde terminee avec succes !")
        print(f"Fichier cree : {chemin_complet}")
        
        # Taille du fichier
        taille = os.path.getsize(chemin_complet)
        if taille < 1024:
            print(f"Taille : {taille} octets")
        elif taille < 1024*1024:
            print(f"Taille : {taille/1024:.2f} Ko")
        else:
            print(f"Taille : {taille/(1024*1024):.2f} Mo")
        
    except Exception as e:
        print(f"Erreur pendant la sauvegarde : {e}")
    
    finally:
        # Fermer la connexion
        if connexion:
            connexion.close()
            print("Connexion fermee")
    
    print("="*60 + "\n")

# ============================================
# POINT D'ENTREE
# ============================================
if __name__ == "__main__":
    main()
