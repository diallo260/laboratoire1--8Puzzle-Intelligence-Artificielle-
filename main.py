# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203)

import os
import sys

import mesures
import puzzle
from bfs import bfs
from dfs import dfs
from iddfs import iddfs

DOSSIER_ENTREES = "entree"
DOSSIER_CHEMINS = "chemins"
NB_EXECUTIONS = 10
APERCU_CHEMIN = 20

ALGORITHMES = [
    ("BFS", bfs),
    ("DFS", dfs),
    ("IDDFS", iddfs),
]


def ecrire_chemin(chemin, nom_algo, nom_entree):
    """Enregistre le chemin d'actions dans un fichier dedie.

    Un seul fichier par algorithme et par entree : les algorithmes etant
    deterministes, les 10 executions produisent le meme chemin.
    """
    os.makedirs(DOSSIER_CHEMINS, exist_ok=True)
    chemin_fichier = os.path.join(
        DOSSIER_CHEMINS, f"{nom_algo}_{nom_entree}_chemin.txt"
    )

    with open(chemin_fichier, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{len(chemin)}\n")
        for action in chemin:
            f.write(f"{action}\n")

    return chemin_fichier


def executer(nom_algo, fonction, nom_entree, etat):
    """Lance NB_EXECUTIONS fois l'algorithme et ecrit un fichier par execution."""
    temps_cumules = []
    chemin_final = None

    for execution in range(1, NB_EXECUTIONS + 1):
        chemin, stats = fonction(etat)
        mesures.ecrire(stats, nom_algo, nom_entree, execution)
        temps_cumules.append(stats.temps)
        chemin_final = chemin

        print(f"  {nom_algo:<5} exec {execution:>2}/{NB_EXECUTIONS} : "
              f"{stats.etats_explores:>8} etats | {stats.temps:7.3f} s")

    moyenne = sum(temps_cumules) / len(temps_cumules)

    if chemin_final is None:
        print(f"  -> {nom_algo} : echec, temps moyen {moyenne:.3f} s\n")
    else:
        fichier = ecrire_chemin(chemin_final, nom_algo, nom_entree)
        apercu = " ".join(chemin_final[:APERCU_CHEMIN])
        suite = " ..." if len(chemin_final) > APERCU_CHEMIN else ""
        print(f"  -> {nom_algo} : {len(chemin_final)} coups, "
              f"temps moyen {moyenne:.3f} s")
        print(f"     debut du chemin : {apercu}{suite}")
        print(f"     chemin enregistre dans {fichier}\n")

    return chemin_final


def traiter_entree(nom_entree):
    chemin_fichier = os.path.join(DOSSIER_ENTREES, f"{nom_entree}.txt")
    etat = puzzle.lire_etat(chemin_fichier)

    print(f"===== {nom_entree} =====")
    print(puzzle.formater(etat))
    print(f"soluble : {puzzle.est_soluble(etat)}\n")

    for nom_algo, fonction in ALGORITHMES:
        executer(nom_algo, fonction, nom_entree, etat)


def main():
    if len(sys.argv) > 1:
        entrees = sys.argv[1:]
    else:
        entrees = ["Ex1-1", "Ex1-2", "Ex1-3", "Ex1-4"]

    for nom_entree in entrees:
        traiter_entree(nom_entree)


if __name__ == "__main__":
    main()