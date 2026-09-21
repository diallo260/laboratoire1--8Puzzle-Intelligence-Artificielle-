# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203) et Adama A Balde (BALA27070105)

# deuxieme algo : recherche en profondeur (DFS).
# Le DFS plonge le plus loin possible dans une branche avant de revenir en
# arriere. Il trouve une solution si elle existe, mais rien ne garantit que
# ce soit la plus courte : il s'arrete sur la premiere qu'il rencontre, peu
# importe sa longueur. Dans nos essais, il a trouve des chemins de plus de
# 60 000 coups pour des puzzles qui se resolvent en moins de 30.

import time

import puzzle
from recherche import Noeud, Statistiques, remonter_chemin


def dfs(etat_initial):
    # Resout le puzzle par une recherche en profondeur.
    # Retourne un couple (chemin, statistiques). Le chemin est la liste des
    # actions a effectuer, ou None si le puzzle n'a pas de solution.

    # Nous avions d'abord ajoute une limite de profondeur, mais elle faisait
    # echouer l'algorithme sur des puzzles solubles. Elle n'est pas necessaire :
    # l'ensemble des etats visites empeche de traiter deux fois le meme etat,
    # et le nombre d'etats atteignables est fini (181 440). La recherche se
    # termine donc toujours.

    stats = Statistiques()
    # Le chronometre ne couvre que la recherche elle-meme.
    debut = time.perf_counter()

    # La recherche commence a partir de l'etat initial.
    racine = Noeud(etat_initial)

    # La frontiere est une pile (LIFO) : on retire toujours l'etat ajoute le
    # plus recemment. C'est la seule vraie difference avec le BFS, et c'est
    # elle qui fait descendre l'algorithme en profondeur. Une simple liste
    # Python suffit, car ajouter et retirer a la fin est immediat.
    frontiere = [racine]

    # Ensemble des etats deja rencontres. Sans lui, l'algorithme pourrait
    # tourner en rond indefiniment : chaque mouvement est reversible, donc il
    # pourrait aller a gauche, puis a droite, puis a gauche, sans fin.
    visites = {puzzle.cle(etat_initial)}

    # Tant qu'il reste des etats a examiner, la recherche continue.
    while frontiere:
        # On enregistre la taille de la frontiere au debut de l'iteration.
        stats.enregistrer_iteration(len(frontiere))

        # On retire l'etat le plus recent de la pile.
        noeud = frontiere.pop()

        # On teste l'objectif au moment ou l'etat sort de la frontiere,
        # comme dans les deux autres algorithmes.
        if puzzle.est_objectif(noeud.etat):
            stats.temps = time.perf_counter() - debut
            return remonter_chemin(noeud), stats

        # On genere tous les etats atteignables en un coup.
        for action, suivant in puzzle.voisins(noeud.etat):
            k = puzzle.cle(suivant)

            # Si cet etat a deja ete rencontre, on l'ignore.
            if k in visites:
                continue

            # L'etat est marque comme visite pour toute la duree de la
            # recherche. C'est ce qui explique pourquoi les chemins trouves
            # sont si longs : un etat atteint une premiere fois par une
            # branche tres profonde ne pourra plus etre atteint plus tard par
            # un chemin plus court.
            visites.add(k)

            # On cree le noeud enfant et on le pose sur le dessus de la pile.
            # Il sera donc le prochain a etre examine.
            frontiere.append(Noeud(suivant, noeud, action))

    # Si la pile se vide sans trouver l'objectif, tous les etats atteignables
    # ont ete explores : le puzzle n'a pas de solution.
    stats.temps = time.perf_counter() - debut
    return None, stats