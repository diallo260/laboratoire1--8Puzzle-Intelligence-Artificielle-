# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203)

import time

import puzzle
from recherche import Noeud, Statistiques, remonter_chemin


def dfs(etat_initial):
    """Recherche en profondeur. Renvoie (chemin, statistiques).

    L'ensemble des etats visites garantit la terminaison : chaque etat
    n'est empile qu'une seule fois, et l'espace accessible est fini.
    Aucune limite de profondeur n'est donc necessaire.
    """
    stats = Statistiques()
    debut = time.perf_counter()

    racine = Noeud(etat_initial)
    frontiere = [racine]
    visites = {puzzle.cle(etat_initial)}

    while frontiere:
        stats.enregistrer_iteration(len(frontiere))
        noeud = frontiere.pop()

        if puzzle.est_objectif(noeud.etat):
            stats.temps = time.perf_counter() - debut
            return remonter_chemin(noeud), stats

        for action, suivant in puzzle.voisins(noeud.etat):
            k = puzzle.cle(suivant)
            if k in visites:
                continue
            visites.add(k)
            frontiere.append(Noeud(suivant, noeud, action))

    stats.temps = time.perf_counter() - debut
    return None, stats