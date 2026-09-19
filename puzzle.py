# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203)

import numpy as np

# Etat objectif : 1 2 3 / 4 5 6 / 7 8 _   (0 represente la case vide)
ETAT_OBJECTIF = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0], dtype=np.int8).reshape(9, 1)

# Les 12 paires de cases adjacentes dans la grille 3x3
# Index des cases :  0 1 2
#                    3 4 5
#                    6 7 8
PAIRES_ADJACENTES = [
    (0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8),   # horizontales
    (0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8),   # verticales
]


def _matrice_permutation(i, j):
    """Matrice identite 9x9 dont les lignes i et j sont interverties.
    Appliquee a un vecteur colonne, elle echange les composantes i et j."""
    p = np.eye(9, dtype=np.int8)
    p[[i, j]] = p[[j, i]]
    return p


def _nom_action(depart, arrivee):
    """Nom du mouvement de la CASE VIDE, de la position depart vers arrivee."""
    ecart = arrivee - depart
    if ecart == -3:
        return "haut"
    if ecart == 3:
        return "bas"
    if ecart == -1:
        return "gauche"
    return "droite"


def _construire_mouvements():
    """MOUVEMENTS[p] = liste des (nom, matrice) applicables quand le vide est en p."""
    table = {p: [] for p in range(9)}
    for i, j in PAIRES_ADJACENTES:
        m = _matrice_permutation(i, j)
        table[i].append((_nom_action(i, j), m))   # vide en i, part vers j
        table[j].append((_nom_action(j, i), m))   # vide en j, part vers i
    return table


MOUVEMENTS = _construire_mouvements()


def lire_etat(chemin):
    """Lit une grille 3x3 dans un fichier et renvoie un vecteur colonne 9x1."""
    with open(chemin, 'r', encoding='utf-8') as f:
        lignes = f.read().splitlines()

    valeurs = []
    for ligne in lignes:
        if not ligne.strip():
            continue
        for case in ligne.split('\t'):
            case = case.strip()
            valeurs.append(0 if case == '' else int(case))

    if len(valeurs) != 9:
        raise ValueError(f"{chemin} : {len(valeurs)} valeurs au lieu de 9")
    if sorted(valeurs) != list(range(9)):
        raise ValueError(f"{chemin} : les valeurs ne sont pas exactement 0 a 8")

    return np.array(valeurs, dtype=np.int8).reshape(9, 1)


def cle(etat):
    """Cle immuable et hachable, utilisable dans un set."""
    return etat.tobytes()


def position_vide(etat):
    return int(np.argmax(etat == 0))


def voisins(etat):
    """Liste des (nom_action, nouvel_etat) atteignables en un coup."""
    resultat = []
    for nom, matrice in MOUVEMENTS[position_vide(etat)]:
        resultat.append((nom, matrice @ etat))
    return resultat


def est_objectif(etat):
    return np.array_equal(etat, ETAT_OBJECTIF)


def est_soluble(etat):
    """Un 8-puzzle est soluble si son nombre d'inversions est pair."""
    tuiles = [int(v) for v in etat.flatten() if v != 0]
    inversions = sum(
        1
        for a in range(len(tuiles))
        for b in range(a + 1, len(tuiles))
        if tuiles[a] > tuiles[b]
    )
    return inversions % 2 == 0


def formater(etat):
    """Representation lisible d'un etat, pour l'affichage."""
    v = etat.flatten()
    lignes = []
    for r in range(3):
        cases = []
        for c in range(3):
            valeur = int(v[r * 3 + c])
            cases.append('_' if valeur == 0 else str(valeur))
        lignes.append(' '.join(cases))
    return '\n'.join(lignes)