#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# NTL-SysToolbox - Audit d'Obsolescence
# Source : https://endoflife.date/api

import csv
import json
import os
import sys
import platform
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# URL de l'API endoflife.date 
API_BASE = "https://endoflife.date/api"

OS_ALIASES = {
    "ubuntu": "ubuntu",
    "debian": "debian",
    "windows": "windows",
    "windows server": "windows-server",
    "windows-server": "windows-server",
    "android": "android",
    "macos": "macos",
    "ios": "ios",
    "almalinux": "almalinux",
    "rocky": "rocky-linux",
    "rocky linux": "rocky-linux",
    "oracle linux": "oracle-linux",
    "mx linux": "mxlinux"
}


def detect_local_os():
    """
    Détecte automatiquement l'OS et la version de la machine locale.
    Fonctionne sur Linux et Windows.
    """
    system = platform.system()

    if system == "Linux":
        # Lecture de /etc/os-release (standard sur Ubuntu, Debian, etc.)
        if os.path.exists("/etc/os-release"):
            info = {}
            with open("/etc/os-release") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line:
                        key, value = line.split("=", 1)
                        info[key] = value.strip('"')
            name    = info.get("ID", "linux").lower()
            version = info.get("VERSION_ID", "")
            return name, version
    elif system == "Windows":
        version = platform.version()
        release = platform.release()
        return "windows", release

    return platform.system().lower(), platform.release()


def normalize_os_name(user_input: str) -> str:
    value = user_input.strip().lower()
    return OS_ALIASES.get(value, value.replace(" ", "-"))


def fetch_os_lifecycle(os_slug: str):
    """Appelle l'API endoflife.date et retourne la liste des versions."""
    url = f"{API_BASE}/{os_slug}.json"
    req = Request(url, headers={"User-Agent": "NTL-SysToolbox/1.0"})
    try:
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))

            if isinstance(data, list):
                return data

            if isinstance(data, dict):
                for key in ("cycles", "releases", "results", "result"):
                    if isinstance(data.get(key), list):
                        return data[key]
                values = list(data.values())
                if values and all(isinstance(v, dict) for v in values):
                    return values

            print(f"[AVERT] Format inattendu : {str(data)[:200]}")
            return []

    except HTTPError as e:
        if e.code == 404:
            print(f"[ERREUR] OS inconnu ou non supporté : {os_slug}")
        else:
            print(f"[ERREUR] HTTP {e.code}")
        sys.exit(1)
    except URLError as e:
        print(f"[ERREUR] Impossible de contacter l'API : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERREUR] Réponse invalide : {e}")
        sys.exit(1)


def extract_release_info(item: dict):
    """Extrait les infos utiles d'une version."""
    version = (
        item.get("cycle")
        or item.get("releaseCycle")
        or item.get("release")
        or item.get("name")
        or "Inconnue"
    )
    eol = item.get("eol") or item.get("eolFrom") or "Non renseignée"
    release_date = item.get("releaseDate") or item.get("released") or ""
    latest = item.get("latest") or ""
    lts = item.get("lts", False)

    return {
        "version": str(version),
        "release_date": str(release_date),
        "eol_date": str(eol),
        "latest": str(latest),
        "lts": "Oui" if lts else "Non"
    }


def display_versions(os_name: str, rows: list):
    """Affiche les versions dans le terminal."""
    print("\n" + "=" * 70)
    print(f"  Audit d'obsolescence - {os_name}")
    print("=" * 70)
    print(f"{'Version':<20} {'Release':<15} {'Fin de vie':<15} {'Latest':<12} {'LTS'}")
    print("-" * 70)
    for row in rows:
        print(
            f"{row['version']:<20} "
            f"{row['release_date']:<15} "
            f"{row['eol_date']:<15} "
            f"{row['latest']:<12} "
            f"{row['lts']}"
        )
    print("-" * 70)
    print(f"Total : {len(rows)} versions")
    print("=" * 70 + "\n")


def export_results(os_slug: str, rows: list):
    """Exporte les résultats en CSV et JSON."""
    default_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    output_dir = input(f"Dossier d'export [{default_dir}] : ").strip() or default_dir
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path  = os.path.join(output_dir, f"audit_{os_slug}_{timestamp}.csv")
    json_path = os.path.join(output_dir, f"audit_{os_slug}_{timestamp}.json")

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["version", "release_date", "eol_date", "latest", "lts"])
        for row in rows:
            writer.writerow([row["version"], row["release_date"], row["eol_date"], row["latest"], row["lts"]])

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "module": "audit_obso",
            "os": os_slug,
            "generated_at": datetime.now().isoformat(),
            "versions": rows
        }, f, indent=4, ensure_ascii=False)

    print(f"CSV  : {csv_path}")
    print(f"JSON : {json_path}\n")


def audo():
    print("\n" + "=" * 60)
    print("          NTL-SysToolbox - Audit d'Obsolescence")
    print("=" * 60)

    # Détection automatique de l'OS local
    local_os, local_version = detect_local_os()
    print(f"  OS détecté : {local_os} {local_version}")
    choix_auto = input(f"  Auditer cet OS ? (o/n) : ").strip().lower()

    if choix_auto in ("o", "oui", "y", "yes"):
        os_input = local_os
    else:
        os_input = input("OS à auditer (ex: ubuntu, debian, windows) : ").strip()

    if not os_input:
        print("[ERREUR] Aucun OS saisi.")
        return

    os_slug  = normalize_os_name(os_input)
    raw_data = fetch_os_lifecycle(os_slug)
    rows     = [extract_release_info(item) for item in raw_data]

    if not rows:
        print("[ERREUR] Aucune version trouvée.")
        return

    display_versions(os_input, rows)

    # Si on a audité l'OS local, on indique si la version est supportée
    if choix_auto in ("o", "oui", "y", "yes") and local_version:
        version_courte = local_version.split(".")[0]  # ex: "20" pour "20.04"
        for row in rows:
            if row["version"].startswith(version_courte):
                eol = row["eol_date"]
                print(f"  ⚠  Votre version ({local_version}) → Fin de vie : {eol}")
                break

    choix = input("Exporter en CSV/JSON ? (o/n) : ").strip().lower()
    if choix in ("o", "oui", "y", "yes"):
        export_results(os_slug, rows)


if __name__ == "__main__":
    audo()
