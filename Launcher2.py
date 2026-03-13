import os
import sys
import time
import random
import subprocess

R = "\033[0m"

def fg(code):      return f"\033[38;5;{code}m"
def bold(t):       return f"\033[1m{t}{R}"
def col(code, t):  return f"{fg(code)}{t}{R}"

def strip_ansi(s):
    import re
    return re.sub(r'\033\[[0-9;]*m', '', s)

def vlen(s):
    return len(strip_ansi(s))

THEMES = [
    ("Ocean Bleu",        39,    51,    15,   244,   45),
    ("Foret Emeraude",    35,   118,    15,   244,   46),
    ("Coucher de Soleil", 202,  214,    15,   244,  208),
    ("Violet Cosmos",     135,  177,    15,   244,  141),
    ("Rose Neon",         198,  205,    15,   244,  213),
    ("Glace Arctique",     75,  153,    15,   244,  123),
    ("Or Imperial",       220,  227,    15,   244,  226),
    ("Rouge Lave",        196,  203,    15,   244,  202),
]

def pick_theme():
    return random.choice(THEMES)

LOGO_LINES = [
    "  XX  XXXXXXXXXXX XX     ",
    "  XXX XX  XX  XX  XX     ",
    "  XX XXX  XX  XX  XX     ",
    "  XX  XX  XX  XX  XX     ",
    "  XX   X  XX  XX  XXXXXXX",
    "  XX      XX  XX  XXXXXXX",
]

LOGO_REAL = [
    "  \u2588\u2588\u2557  \u2588\u2588\u2557\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2557     ",
    "  \u2588\u2588\u2588\u2557\u2588\u2588\u2554\u255d\u255a\u2550\u2550\u2588\u2588\u2554\u2550\u2550\u255d\u2588\u2588\u2551     ",
    "  \u2588\u2588\u2554\u2588\u2588\u2588\u2554\u255d    \u2588\u2588\u2551   \u2588\u2588\u2551     ",
    "  \u2588\u2588\u2551\u255a\u2588\u2588\u2554\u255d    \u2588\u2588\u2551   \u2588\u2588\u2551     ",
    "  \u2588\u2588\u2551 \u255a\u2588\u2588\u2557    \u2588\u2588\u2551   \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557",
    "  \u255a\u2550\u255d  \u255a\u2550\u255d    \u255a\u2550\u255d   \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u255d",
]

def tw():
    try:    return max(88, os.get_terminal_size().columns)
    except: return 100

def spinner(msg, duration=0.7, ac=39):
    frames = ["\u280b","\u2819","\u2839","\u2838","\u283c","\u2834","\u2826","\u2827","\u2807","\u280f"]
    end_t = time.time() + duration
    i = 0
    sys.stdout.write("\n")
    while time.time() < end_t:
        sys.stdout.write("\r  " + col(ac, frames[i % len(frames)]) + "  " + col(244, msg) + "  ")
        sys.stdout.flush()
        time.sleep(0.07)
        i += 1
    sys.stdout.write("\r  " + col(82, "\u2714") + "  " + col(252, msg) + "  \n")
    sys.stdout.flush()

def progress(label, PW=28, duration=0.45, c1=39, c2=240):
    sys.stdout.write("\n")
    for i in range(PW + 1):
        pct = int(i / PW * 100)
        bar = fg(c1) + "\u2588" * i + fg(c2) + "\u2591" * (PW - i) + R
        sys.stdout.write("\r  " + col(c2, label) + "  [" + bar + "]  " + col(c1, str(pct).rjust(3) + "%"))
        sys.stdout.flush()
        time.sleep(duration / PW)
    sys.stdout.write("\n\n")
    sys.stdout.flush()

def top_bar(w, title, ver, bc, tc):
    title_s = " " + col(bc, "\u2500"*3) + " " + bold(col(tc, title)) + " " + col(bc, "\u2500") + " " + col(244, ver) + " "
    tlen    = 3 + 1 + len(title) + 1 + 1 + 1 + len(ver) + 1 + 3
    rest    = w - 2 - tlen
    return col(bc, "\u256d") + title_s + col(bc, "\u2500" * max(rest, 0)) + col(bc, "\u256e")

def bot_bar(w, info, bc, dc):
    info_s = " " + col(dc, info) + " "
    ilen   = len(info) + 2
    rest   = w - 2 - ilen
    return col(bc, "\u2570") + info_s + col(bc, "\u2500" * max(rest, 0)) + col(bc, "\u256f")

def div_row(lw, rw, bc):
    return col(bc, "\u251c") + col(bc, "\u2500"*lw) + col(bc, "\u253c") + col(bc, "\u2500"*rw) + col(bc, "\u2524")

def row(left_cell, right_cell, lw, rw, bc):
    lpad = lw - vlen(left_cell)
    rpad = rw - vlen(right_cell)
    return (col(bc, "\u2502") + left_cell + " " * max(lpad, 0)
          + col(bc, "\u2502") + right_cell + " " * max(rpad, 0) + col(bc, "\u2502"))

def blank_row(lw, rw, bc):
    return row("", "", lw, rw, bc)

MENU = {
    1: {"title": "Diagnostics Systemes",  "path": "Diagnostics/diag_system.py",  "icon": "[SYS]", "desc": "CPU - RAM - Reseau - Disque"},
    2: {"title": "Sauvegardes WMS",        "path": "Sauv_wms/wms_save.py",        "icon": "[SAV]", "desc": "Backup - Restore - Planification"},
    3: {"title": "Audit d'Obsolescence",   "path": "Audit_Obso/audit_obso.py",    "icon": "[AUD]", "desc": "Detection - Rapport - Alertes"},
}

def display_menu(theme, base_dir):
    os.system("cls" if os.name == "nt" else "clear")
    t_name, bc, ac, tc, dc, lc = theme
    W  = min(tw(), 104)
    LW = 36
    RW = W - LW - 3

    lines = []
    lines.append(top_bar(W, "NTL-SysToolbox", "v1.0", bc, tc))

    l_hdr = "  " + bold(col(ac, "\u25c8  Panneau de Controle"))
    r_hdr = "  " + col(dc, "Theme :") + "  " + col(ac, t_name)
    lines.append(row(l_hdr, r_hdr, LW, RW, bc))

    now_s  = time.strftime("%A %d %b %Y  -  %H:%M:%S")
    path_s = ("..." + base_dir[-(RW-6):]) if len(base_dir) > RW - 5 else base_dir
    lines.append(row("  " + col(dc, now_s), "  " + col(dc, path_s), LW, RW, bc))
    lines.append(div_row(LW, RW, bc))
    lines.append(blank_row(LW, RW, bc))

    menu_title_shown = False
    for ll in LOGO_REAL:
        left_cell  = "  " + col(lc, ll)
        right_cell = ("  " + bold(col(tc, "  Options disponibles"))) if not menu_title_shown else ""
        menu_title_shown = True
        lines.append(row(left_cell, right_cell, LW, RW, bc))

    lines.append(blank_row(LW, RW, bc))
    lines.append(div_row(LW, RW, bc))

    left_col = [
        "  " + col(ac, "\u25cf") + " " + bold(col(tc, "Systeme")),
        "  " + col(dc, "NTL-SysToolbox"),
        "  " + col(dc, "Python " + sys.version.split()[0]),
        "",
        "  " + col(ac, "\u25cf") + " " + bold(col(tc, "Statut")),
        "  " + col(82, "\u25c9") + "  " + col(dc, "Operationnel"),
        "",
        "  " + col(ac, "\u25cf") + " " + bold(col(tc, "Raccourci")),
        "  " + col(dc, "[0]  ->  Quitter"),
    ]

    right_col = []
    for key, opt in MENU.items():
        right_col.append(
            "  " + bold(col(bc, "[")) + bold(col(ac, str(key))) + bold(col(bc, "]"))
            + "  " + col(ac, opt["icon"]) + "  " + bold(col(tc, opt["title"]))
        )
        right_col.append("       " + col(dc, ">  " + opt["desc"]))
        right_col.append("")

    max_r = max(len(left_col), len(right_col))
    for i in range(max_r):
        lv = left_col[i]  if i < len(left_col)  else ""
        rv = right_col[i] if i < len(right_col) else ""
        lines.append(row(lv, rv, LW, RW, bc))

    lines.append(blank_row(LW, RW, bc))
    lines.append(bot_bar(W, "choisir un numero  |  Entree valider  |  Ctrl+C quitter", bc, dc))

    print()
    for l in lines:
        print(l)
    print()
    return input("  " + col(bc, "\u2570\u2500\u25b6") + "  " + bold(col(ac, "Selection")) + "  " + col(dc, ":") + "  ").strip()

def run_script(base_dir, path, title, icon, theme):
    t_name, bc, ac, tc, dc, lc = theme
    script = os.path.abspath(os.path.join(base_dir, path))
    W      = min(tw(), 104)

    os.system("cls" if os.name == "nt" else "clear")
    print()
    print(top_bar(W, icon + "  " + title, "", bc, tc))

    if not os.path.exists(script):
        pad = W - 2
        line1 = "  " + col(196, "\u2718") + "  " + col(252, "Fichier introuvable :")
        print(col(bc, "\u2502") + line1 + " " * max(pad - vlen(line1), 0) + col(bc, "\u2502"))
        short = script if len(script) < pad - 5 else "..." + script[-(pad-8):]
        line2 = "  " + col(dc, short)
        print(col(bc, "\u2502") + line2 + " " * max(pad - vlen(line2), 0) + col(bc, "\u2502"))
        print(bot_bar(W, "Erreur - fichier manquant", bc, dc))
        return

    progress("Demarrage : " + title[:28], c1=ac, c2=dc)

    divider = col(bc, "\u2502") + "  " + col(dc, "\u2500"*(W-5)) + col(bc, "\u2502")
    print(divider)
    print()
    try:
        subprocess.run([sys.executable, script], check=False)
    except KeyboardInterrupt:
        msg = "Script interrompu."
        print("\n  " + col(214, "\u26a0") + "  " + col(252, msg))
    except Exception as e:
        err = str(e)
        print("\n  " + col(196, "\u2718") + "  " + col(252, "Erreur : " + err))

    print()
    print(divider)
    pad2  = W - 2
    ok    = "  " + col(82, "\u2714") + "  " + col(dc, "Execution terminee - retour au menu.")
    print(col(bc, "\u2502") + ok + " " * max(pad2 - vlen(ok), 0) + col(bc, "\u2502"))
    print(bot_bar(W, "NTL-SysToolbox  |  " + title, bc, dc))
    print()

def boot(theme):
    _, bc, ac, tc, dc, lc = theme
    os.system("cls" if os.name == "nt" else "clear")
    print()
    spinner("Chargement des modules",           0.65, ac)
    spinner("Verification de l'environnement",  0.50, ac)
    spinner("Initialisation de l'interface",    0.40, ac)
    time.sleep(0.15)

def farewell(theme):
    t_name, bc, ac, tc, dc, lc = theme
    W = min(tw(), 104)
    os.system("cls" if os.name == "nt" else "clear")
    print()
    print(top_bar(W, "Au revoir", "", bc, tc))
    pad = W - 2
    for _ in range(2):
        print(col(bc, "\u2502") + " " * pad + col(bc, "\u2502"))
    msg = "  " + bold(col(tc, "  Session NTL-SysToolbox terminee - a bientot !"))
    print(col(bc, "\u2502") + msg + " " * max(pad - vlen(msg), 0) + col(bc, "\u2502"))
    sub = "  " + col(dc, "Theme : ") + col(ac, t_name) + "  |  " + col(dc, time.strftime("%H:%M:%S"))
    print(col(bc, "\u2502") + sub + " " * max(pad - vlen(sub), 0) + col(bc, "\u2502"))
    for _ in range(2):
        print(col(bc, "\u2502") + " " * pad + col(bc, "\u2502"))
    print(bot_bar(W, "NTL-SysToolbox  v1.0", bc, dc))
    print()

class CLIInterface:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.theme    = pick_theme()

    def run(self):
        boot(self.theme)
        _, bc, ac, tc, dc, lc = self.theme

        while True:
            try:
                choice = display_menu(self.theme, self.base_dir)
            except KeyboardInterrupt:
                farewell(self.theme)
                sys.exit(0)

            if choice == "0":
                farewell(self.theme)
                break

            try:
                c_int = int(choice)
            except ValueError:
                invalid_msg = "Entree invalide : [" + choice + "] - tapez un chiffre."
                print("\n  " + col(214, "\u26a0") + "  " + col(252, invalid_msg))
                time.sleep(1.3)
                continue

            if c_int in MENU:
                opt = MENU[c_int]
                run_script(self.base_dir, opt["path"], opt["title"], opt["icon"], self.theme)
                input("  " + col(bc, "\u2570\u2500\u25b6") + "  " + col(dc, "Appuyez sur ") + col(ac, "Entree") + col(dc, " pour revenir au menu..."))
            else:
                bad_msg = "Option [" + str(c_int) + "] inexistante. Choisissez entre 0 et " + str(max(MENU)) + "."
                print("\n  " + col(214, "\u26a0") + "  " + col(252, bad_msg))
                time.sleep(1.3)

if __name__ == "__main__":
    try:
        CLIInterface().run()
    except KeyboardInterrupt:
        sys.exit(0)
