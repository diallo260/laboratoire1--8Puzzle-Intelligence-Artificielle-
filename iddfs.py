# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203) et Adama A Balde (BALA27070105)

# troisieme algo : recherche a approfondissement iteratif (IDDFS).
# L'idee est de combiner les avantages des deux autres algorithmes. On lance
# une recherche en profondeur limitee a 0 coup, puis a 1 coup, puis a 2, et
# ainsi de suite jusqu'a trouver l'objectif. Comme la limite augmente de un
# en un, la premiere solution trouvee est forcement la plus courte, comme
# avec le BFS. Et comme chaque passe est une recherche en profondeur, la
# frontiere reste petite, comme avec le DFS. Le prix a payer est le temps :
# chaque nouvelle passe recommence la recherche depuis le debut.

import time

import puzzle
from recherche import Noeud, Statistiques, remonter_chemin

# Toute configuration soluble du 8-puzzle se resout en 31 coups au maximum.
# Il est donc inutile d'aller plus loin : si aucune solution n'est trouvee a
# la limite 31, le puzzle n'en a pas.
LIMITE_MAX = 31


def _dfs_limite(racine, limite, stats):
    # Recherche en profondeur qui ne descend pas au-dela d'une limite donnee.
    # Retourne le noeud objectif s'il est trouve, sinon None.
    # Pour eviter de refaire trop de travail, on memorise pour chaque etat la
    # plus petite profondeur a laquelle on l'a atteint pendant cette passe. Un
    # etat n'est reexplore que si on l'atteint a une profondeur strictement
    # plus courte que la meilleure connue : arriver plus tot laisse plus de
    # coups disponibles pour la suite, donc aucune solution n'est perdue.

    # Comme pour le DFS, la frontiere est une pile.
    frontiere = [racine]

    # Dictionnaire qui associe a chaque etat la plus petite profondeur a
    # laquelle il a ete atteint dans cette passe. Il est recree a chaque
    # appel, donc a chaque nouvelle limite : une information obtenue avec la
    # limite 5 n'a plus de sens avec la limite 12.
    vus = {puzzle.cle(racine.etat): 0}

    while frontiere:
        # Les mesures sont accumulees sur toutes les passes de l'IDDFS,
        # puisqu'une execution de l'algorithme comprend toutes ces passes.
        stats.enregistrer_iteration(len(frontiere))

        # On retire l'etat le plus recent de la pile.
        noeud = frontiere.pop()

        # On teste l'objectif au moment ou l'etat sort de la frontiere,
        # comme dans les deux autres algorithmes.
        if puzzle.est_objectif(noeud.etat):
            return noeud

        # Si le noeud a deja atteint la limite de profondeur, on ne genere
        # pas ses enfants : ils seraient au-dela de ce qu'on s'autorise dans
        # cette passe.
        if noeud.profondeur >= limite:
            continue

        # On genere tous les etats atteignables en un coup.
        for action, suivant in puzzle.voisins(noeud.etat):
            k = puzzle.cle(suivant)
            profondeur_enfant = noeud.profondeur + 1

            # Si l'etat a deja ete atteint a une profondeur egale ou plus
            # petite, le reexplorer ne peut rien apporter de nouveau.
            if k in vus and vus[k] <= profondeur_enfant:
                continue

            # Sinon, on retient cette nouvelle meilleure profondeur et on
            # ajoute l'etat a la pile.
            vus[k] = profondeur_enfant
            frontiere.append(Noeud(suivant, noeud, action))

    # La pile est vide : aucune solution a moins de "limite" coups.
    return None


def iddfs(etat_initial, limite_max=LIMITE_MAX):
    # Resout le puzzle par approfondissement iteratif.
    # Retourne un couple (chemin, statistiques). Le chemin est la liste des
    # actions a effectuer, ou None si le puzzle n'a pas de solution.
    # Un seul objet de statistiques pour toute l'execution : les mesures de
    # chaque passe s'ajoutent les unes a la suite des autres.
    stats = Statistiques()

    # Le chronometre couvre l'ensemble des passes.
    debut = time.perf_counter()

    # On essaie les limites 0, 1, 2, ... jusqu'a LIMITE_MAX inclus.
    for limite in range(limite_max + 1):

        # Chaque passe repart de l'etat initial.
        racine = Noeud(etat_initial)
        trouve = _dfs_limite(racine, limite, stats)

        # Des qu'une passe trouve l'objectif, on s'arrete. Comme les limites
        # ont ete essayees dans l'ordre croissant, ce chemin est le plus court.
        if trouve is not None:
            stats.temps = time.perf_counter() - debut
            return remonter_chemin(trouve), stats

    # Aucune passe n'a trouve l'objectif, meme a la limite maximale : le
    # puzzle n'a pas de solution. C'est le cas de l'entree Ex1-3, qui oblige
    # l'algorithme a epuiser les 32 passes et explique son temps tres long.
    stats.temps = time.perf_counter() - debut
    return None, stats