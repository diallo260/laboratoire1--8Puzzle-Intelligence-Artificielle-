# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203) et Adama A Balde (BALA27070105)

# fichier d'execution du programme : Ce fichier ne contient aucun algorithme : il
# # lit les entrees, lance chaque algorithme dix fois sur chacune d'elles,
# # ecrit les fichiers de mesures et affiche un resume dans le terminal.

# fonctionnement :
#   python main.py          traite les quatre entrees
#   python main.py Ex1-1    traite seulement l'entree indiquee

import os
import sys

import mesures
import puzzle
from bfs import bfs
from dfs import dfs
from iddfs import iddfs

# Dossier contenant les fichiers d'etats initiaux fournis avec l'enonce.
DOSSIER_ENTREES = "entree"
# Dossier dans lequel on enregistre les chemins d'actions trouves.
DOSSIER_CHEMINS = "chemins"
# L'enonce demande de reexecuter chaque algorithme dix fois.
NB_EXECUTIONS = 10
# Nombre d'actions affichees dans le terminal pour donner un apercu du chemin.
APERCU_CHEMIN = 20

# Liste des algorithmes a executer, chacun associe au nom utilise dans les
# fichiers de resultats.
ALGORITHMES = [
    ("BFS", bfs),
    ("DFS", dfs),
    ("IDDFS", iddfs),
]


def ecrire_chemin(chemin, nom_algo, nom_entree):
    # Enregistre le chemin d'actions trouve dans un fichier separe.
    # Les chemins ne sont pas ecrits dans les fichiers d'evaluation, pour ne pas
    # modifier le format demande par l'enonce. Ils ne sont pas non plus affiches
    # en entier dans le terminal, car ceux du DFS depassent 60 000 actions.

    # Un seul fichier par algorithme et par entree suffit : les algorithmes sont
    # deterministes, donc les dix executions produisent exactement le meme
    # chemin.

    # On cree le dossier s'il n'existe pas encore.
    os.makedirs(DOSSIER_CHEMINS, exist_ok=True)
    chemin_fichier = os.path.join(
        DOSSIER_CHEMINS, f"{nom_algo}_{nom_entree}_chemin.txt"
    )

    with open(chemin_fichier, "w", encoding="utf-8", newline="\n") as f:
        # La premiere ligne donne le nombre de coups, pour qu'on connaisse la
        # longueur du chemin sans avoir a parcourir tout le fichier.
        f.write(f"{len(chemin)}\n")
        # Ensuite, une action par ligne, dans l'ordre ou il faut les jouer.
        for action in chemin:
            f.write(f"{action}\n")

    return chemin_fichier


def executer(nom_algo, fonction, nom_entree, etat):
    # Lance un algorithme dix fois sur une entree et enregistre les resultats.
    # Les algorithmes etant deterministes, le chemin et le nombre d'etats
    # explores sont les memes a chaque execution. Seul le temps varie, selon
    # l'activite de la machine. C'est pourquoi on calcule une moyenne des temps.


    temps_cumules = []
    chemin_final = None

    for execution in range(1, NB_EXECUTIONS + 1):
        # On lance la recherche sur l'etat initial.
        chemin, stats = fonction(etat)

        # Chaque execution produit son propre fichier de mesures, comme le
        # demande l'enonce.
        mesures.ecrire(stats, nom_algo, nom_entree, execution)

        # On garde le temps pour calculer la moyenne a la fin.
        temps_cumules.append(stats.temps)
        chemin_final = chemin

        # Affichage d'une ligne par execution pour suivre la progression.
        print(f"  {nom_algo:<5} exec {execution:>2}/{NB_EXECUTIONS} : "
              f"{stats.etats_explores:>8} etats | {stats.temps:7.3f} s")

    # Temps moyen sur les dix executions.
    moyenne = sum(temps_cumules) / len(temps_cumules)

    if chemin_final is None:
        # Aucun chemin : le puzzle n'a pas de solution (cas de Ex1-3).
        print(f"  -> {nom_algo} : echec, temps moyen {moyenne:.3f} s\n")
    else:
        # On enregistre le chemin complet dans son fichier.
        fichier = ecrire_chemin(chemin_final, nom_algo, nom_entree)

        # On n'affiche que les premieres actions dans le terminal, suivies de
        # points de suspension si le chemin est plus long.
        apercu = " ".join(chemin_final[:APERCU_CHEMIN])
        suite = " ..." if len(chemin_final) > APERCU_CHEMIN else ""
        print(f"  -> {nom_algo} : {len(chemin_final)} coups, "
              f"temps moyen {moyenne:.3f} s")
        print(f"     debut du chemin : {apercu}{suite}")
        print(f"     chemin enregistre dans {fichier}\n")

    return chemin_final


def traiter_entree(nom_entree):
    # Lit une entree et lui applique les trois algorithmes.
    # Lecture de la grille et conversion en vecteur colonne.
    chemin_fichier = os.path.join(DOSSIER_ENTREES, f"{nom_entree}.txt")
    etat = puzzle.lire_etat(chemin_fichier)

    # On affiche la grille de depart et on indique si elle est soluble. Cette
    # verification ne sert qu'a l'affichage : les algorithmes sont lances
    # dans tous les cas, pour mesurer leur comportement meme sans solution.
    print(f"===== {nom_entree} =====")
    print(puzzle.formater(etat))
    print(f"soluble : {puzzle.est_soluble(etat)}\n")

# on applique chacun des trois algo a cette entree.
    for nom_algo, fonction in ALGORITHMES:
        executer(nom_algo, fonction, nom_entree, etat)


def main():

    # Determine les entrees a traiter puis lance les executions."""
    # L'enonce demande un programme qui prend un etat initial en argument.
    # Si des noms d'entrees sont donnes sur la ligne de commande, on traite
    # seulement celles-ci ; sinon, on traite les quatre entrees fournies.

    if len(sys.argv) > 1:
        entrees = sys.argv[1:]
    else:
        entrees = ["Ex1-1", "Ex1-2", "Ex1-3", "Ex1-4"]

    for nom_entree in entrees:
        traiter_entree(nom_entree)

# Ce bloc ne s'execute que si on lance directement "python main.py", et non
# si le fichier est importe par un autre module.
if __name__ == "__main__":
    main()