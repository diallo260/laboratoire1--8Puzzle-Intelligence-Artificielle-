# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203)

import time
from collections import deque

import puzzle
from recherche import Noeud, Statistiques, remonter_chemin


def bfs(etat_initial):
    """Recherche en largeur. Renvoie (chemin, statistiques).
    chemin vaut None si aucune solution n'existe."""
    stats = Statistiques()
    debut = time.perf_counter()

    racine = Noeud(etat_initial)
    frontiere = deque([racine])
    decouverts = {puzzle.cle(etat_initial)}

    while frontiere:
        stats.enregistrer_iteration(len(frontiere))
        noeud = frontiere.popleft()

        if puzzle.est_objectif(noeud.etat):
            stats.temps = time.perf_counter() - debut
            return remonter_chemin(noeud), stats

        for action, suivant in puzzle.voisins(noeud.etat):
            k = puzzle.cle(suivant)
            if k in decouverts:
                continue
            decouverts.add(k)
            frontiere.append(Noeud(suivant, noeud, action))

    stats.temps = time.perf_counter() - debut
    return None, stats