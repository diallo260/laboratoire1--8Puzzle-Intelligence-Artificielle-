# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203)

import time

import puzzle
from recherche import Noeud, Statistiques, remonter_chemin

LIMITE_MAX = 31


def _dfs_limite(racine, limite, stats):
    """DFS borne a une profondeur. Renvoie le noeud objectif ou None.

    Un etat n'est reexplore que si on l'atteint a une profondeur strictement
    plus courte que la meilleure connu dans cette passe : arriver plus tot
    laisse plus de ressource pour la suite, donc aucune solution n'est perdue.
    """
    frontiere = [racine]
    vus = {puzzle.cle(racine.etat): 0}

    while frontiere:
        stats.enregistrer_iteration(len(frontiere))
        noeud = frontiere.pop()

        if puzzle.est_objectif(noeud.etat):
            return noeud

        if noeud.profondeur >= limite:
            continue

        for action, suivant in puzzle.voisins(noeud.etat):
            k = puzzle.cle(suivant)
            profondeur_enfant = noeud.profondeur + 1
            if k in vus and vus[k] <= profondeur_enfant:
                continue
            vus[k] = profondeur_enfant
            frontiere.append(Noeud(suivant, noeud, action))

    return None


def iddfs(etat_initial, limite_max=LIMITE_MAX):
    """Approfondissement iteratif. Renvoie (chemin, statistiques)."""
    stats = Statistiques()
    debut = time.perf_counter()

    for limite in range(limite_max + 1):
        racine = Noeud(etat_initial)
        trouve = _dfs_limite(racine, limite, stats)
        if trouve is not None:
            stats.temps = time.perf_counter() - debut
            return remonter_chemin(trouve), stats

    stats.temps = time.perf_counter() - debut
    return None, stats