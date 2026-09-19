# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203)

import os

DOSSIER_RESULTATS = "resultats"


def nom_fichier(algorithme, entree, execution):
    """Exemple : BFS_Ex1-1_exec01.txt"""
    return f"{algorithme}_{entree}_exec{execution:02d}.txt"


def ecrire(stats, algorithme, entree, execution, dossier=DOSSIER_RESULTATS):
    """Ecrit un fichier de mesures pour une execution.

    Format :
      - une ligne par iteration : numero_iteration \t taille_de_frontiere
      - avant-derniere ligne    : nombre global d'etats explores
      - derniere ligne          : temps d'execution
    """
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom_fichier(algorithme, entree, execution))

    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        for numero, taille in enumerate(stats.tailles_frontiere, start=1):
            f.write(f"{numero}\t{taille}\n")
        f.write(f"{stats.etats_explores}\n")
        f.write(f"{stats.temps:.6f}\n")

    return chemin