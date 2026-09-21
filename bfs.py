# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203) et Adama A Balde (BALA27070105)

# Premier Algo : recherche en largeur (BFS).
# Le BFS explore l'arbre niveau par niveau : il examine tous les etats a un
# coup de l'etat initial, puis tous ceux a deux coups, et ainsi de suite.
# Grace a cet ordre, la premiere solution qu'il rencontre est forcement la
# plus courte. Son inconvenient est la memoire : la frontiere doit contenir
# un niveau entier de l'arbre, et ce niveau grossit tres vite.

import time
from collections import deque

import puzzle
from recherche import Noeud, Statistiques, remonter_chemin


def bfs(etat_initial):
    # Resout le puzzle par une recherche en largeur.
    # Retourne un couple (chemin, statistiques). Le chemin est la liste des
    # actions a effectuer, ou None si le puzzle n'a pas de solution.

    stats = Statistiques()
    # perf_counter() est l'horloge la plus precise disponible en Python pour
    # mesurer une duree. Le chronometre ne couvre que la recherche elle-meme,
    # pas la lecture du fichier ni l'ecriture des resultats.
    debut = time.perf_counter()

    # La recherche commence a partir de l'etat initial, qui devient la racine.
    racine = Noeud(etat_initial)

    # La frontiere est une file (FIFO) : on retire toujours l'etat le plus
    # ancien. C'est ce qui donne l'exploration niveau par niveau. On utilise
    # deque plutot qu'une liste, car retirer le premier element d'une liste
    # est lent, alors que popleft() sur une deque est immediat.
    frontiere = deque([racine])

    # Ensemble des etats deja rencontres, pour ne jamais traiter deux fois le
    # meme. On y range la cle de l'etat, car un tableau numpy ne peut pas
    # etre place dans un set.
    decouverts = {puzzle.cle(etat_initial)}

    # Tant qu'il reste des etats a examiner, la recherche continue.
    while frontiere:
        # On enregistre la taille de la frontiere au debut de l'iteration,
        # avant d'en retirer quoi que ce soit.
        stats.enregistrer_iteration(len(frontiere))

        # On retire l'etat le plus ancien de la file.
        noeud = frontiere.popleft()

        # Le test de l'objectif est fait au moment ou l'etat sort de la
        # frontiere. Les trois algorithmes font ce test au meme moment, ce
        # qui permet de comparer leurs nombres d'etats explores.
        if puzzle.est_objectif(noeud.etat):
            stats.temps = time.perf_counter() - debut
            return remonter_chemin(noeud), stats

        # On genere tous les etats atteignables en un coup.
        for action, suivant in puzzle.voisins(noeud.etat):
            k = puzzle.cle(suivant)

            # Si cet etat a deja ete rencontre, on l'ignore.
            if k in decouverts:
                continue

            # On marque l'etat comme decouvert des maintenant, au moment ou
            # on l'ajoute a la file, et non au moment ou on le retirera.
            # Sinon, le meme etat pourrait entrer plusieurs fois dans la file
            # avant d'etre traite, et la frontiere grossirait inutilement.
            decouverts.add(k)

            # On cree le noeud enfant en memorisant son parent et l'action
            # qui y mene, puis on le place en fin de file.
            frontiere.append(Noeud(suivant, noeud, action))

    # Si la frontiere se vide sans que l'objectif ait ete trouve, c'est que
    # tous les etats atteignables ont ete explores : le puzzle n'a pas de
    # solution. C'est ce qui se produit avec l'entree Ex1-3.
    stats.temps = time.perf_counter() - debut
    return None, stats