# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203) et Adama A Balde (BALA27070105)
# ce fichier regroupe tout ce qui concerne le puzzle. la facon de presenter un etat, la lecture des fichiers,
# d'entree, les mouvements possibles et quelques outils de verification. les trois algos de basent sur ce fichier
# sans avoir besoin de connaitre enormement de details.
import numpy as np

# Comme demande par le prof, un etat est un vecteur colonne de 9 cases.
# la matrice est lue ligne par ligne, et la case vide est represente pr un zero
# on fixe le type int8 des le debut. tous les etats du programme auront ainsi le meme
# type, ce qui est vraiment indispensable pour pouvoir faire la comparaison.
ETAT_OBJECTIF = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0], dtype=np.int8).reshape(9, 1)

# Pour savoir ou la case vide peut aller, il suffit de connaitre les cases
# voisines dans la grille. En numerotant les cases de 0 a 8 :
#                    0 1 2
#                    3 4 5
#                    6 7 8
# on obtient exactement 12 paires de cases qui se touchent.
PAIRES_ADJACENTES = [
    (0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8),   # voisins sur la meme ligne.
    (0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8),   # voisins sur la meme colonne.
]

# les mouvements sous forme de matrice de permutation.

def _matrice_permutation(i, j):
    #Construit la matrice qui echange les cases i et j d'un etat.
    #deplacer la case vide revient simplement a echanger deux elements du
    #vecteur. Or un echange peut s'ecrire comme une matrice : c'est la matrice
    #identite dans laquelle on a interverti les lignes i et j. En multipliant
    #cette matrice par l'etat, on obtient le nouvel etat.

    # On part de la matrice identite 9x9, qui laisse un etat inchange.
    p = np.eye(9, dtype=np.int8)
    # on fait l'inversion des lignes i et j en une seule instruction numpy.
    p[[i, j]] = p[[j, i]]
    return p


def _nom_action(depart, arrivee):
    # Donne le nom du mouvement de la case vide.
    # On a choisi de nommer les actions selon le deplacement de la case vide,
    # et non selon celui de la tuile. La direction se deduit de l'ecart entre
    # les deux positions dans la numerotation 0 a 8.

    ecart = arrivee - depart
    # un ecart de 3 correspond a un changement de ligne dans la grille .
    if ecart == -3:
        return "haut"
    if ecart == 3:
        return "bas"
    # un ecart de 1 correspond a un deplacement sur la meme ligne.
    if ecart == -1:
        return "gauche"
    return "droite"


def _construire_mouvements():
    # Prepare, pour chaque position de la case vide, la liste des mouvements possibles.
    # Cette table est construite une seule fois au demarrage du programme.
    # Ensuite, pour trouver les voisins d'un etat, il suffira de regarder ou se
    # trouve la case vide et de lire la liste correspondante.

    # une banque avec une liste vide pour chacune des 9 positions.
    table = {p: [] for p in range(9)}
    for i, j in PAIRES_ADJACENTES:
        m = _matrice_permutation(i, j)

    # La meme matrice sert pour les deux sens du mouvement : echanger deux
    # fois les memes cases ramene a l'etat de depart. Seul le nom change.
        table[i].append((_nom_action(i, j), m))   # la case vide va de i vers j
        table[j].append((_nom_action(j, i), m))   # la case vide va de j ver i
    return table

# La table des mouvements est calculee une seule fois, au chargement du fichier.
MOUVEMENTS = _construire_mouvements()

# Lecture d'un fichier d'entree
def lire_etat(chemin):
    # Lit une grille 3x3 dans un fichier et la transforme en vecteur colonne.
    # Dans les fichiers fournis, les cases sont separees par des tabulations et
    # la case vide n'est representee par rien du tout. Il faut donc lire le
    # fichier avec soin pour ne pas perdre cette case vide.

    with open(chemin, 'r', encoding='utf-8') as f:
        # splitlines() permet de retirer les fins de ligne pour tous les formats.
        lignes = f.read().splitlines()

    valeurs = []
    for ligne in lignes:
        # on ignore une possible ligne vide.
        if not ligne.strip():
            continue
        for case in ligne.split('\t'):
            case = case.strip()
# une case sans contenu est la case vide, codee par 0.
            valeurs.append(0 if case == '' else int(case))

    # On verifie que le fichier contient bien une grille valide avant d'aller
    # plus loin. Mieux vaut une erreur claire tout de suite qu'une recherche
    # qui tourne longtemps sur des donnees incorrectes.
    if len(valeurs) != 9:
        raise ValueError(f"{chemin} : {len(valeurs)} valeurs au lieu de 9")

    # Chaque valeur de 0 a 8 doit apparaitre une et une seule fois.
    if sorted(valeurs) != list(range(9)):
        raise ValueError(f"{chemin} : les valeurs ne sont pas exactement 0 a 8")

    # On retourne le vecteur colonne 9x1 demande par le professeur.
    return np.array(valeurs, dtype=np.int8).reshape(9, 1)


def cle(etat):
    # Transforme un etat en une cle utilisable dans un ensemble (set).
    # Python refuse de placer un tableau numpy dans un set, parce qu'un tableau
    # peut etre modifie apres coup. On utilise donc sa version en octets, qui
    # est figee et tres rapide a comparer.

    return etat.tobytes()


def position_vide(etat):
    # Retourne l'indice (0 a 8) ou se trouve la case vide."""
    # etat == 0 donne un tableau de booleens ; argmax renvoie la position du
    # premier True, c'est-a-dire l'unique case vide.
    return int(np.argmax(etat == 0))


def voisins(etat):
    # Retourne tous les etats atteignables en un seul mouvement.
    # Chaque voisin est accompagne du nom de l'action qui permet de l'obtenir,
    # ce qui servira plus tard a reconstruire le chemin de la solution.
    resultat = []
# on lit dans la table les mouvements permis pour cette position du vide.
    for nom, matrice in MOUVEMENTS[position_vide(etat)]:
        # Appliquer le mouvement = multiplier la matrice par le vecteur etat.
        resultat.append((nom, matrice @ etat))
    return resultat


def est_objectif(etat):
    # Indique si l'etat est l'etat final recherche.
    return np.array_equal(etat, ETAT_OBJECTIF)


def est_soluble(etat):
    # Indique si le puzzle peut etre resolu, sans lancer de recherche.
    # On compte les inversions, c'est-a-dire les paires de tuiles placees dans
    # le mauvais ordre. Pour une grille 3x3, le puzzle est soluble seulement si
    # ce nombre est pair. C'est ce qui nous a permis de savoir a l'avance que
    # l'entree Ex1-3 n'a pas de solution.

    # On retire la case vide : elle ne compte pas dans les inversions.
    tuiles = [int(v) for v in etat.flatten() if v != 0]

    inversions = sum(
        1
        for a in range(len(tuiles))
        for b in range(a + 1, len(tuiles))
        if tuiles[a] > tuiles[b]
    )
    return inversions % 2 == 0


def formater(etat):
    # Retourne l'etat sous forme de grille lisible, pour l'affichage.
    # On remet le vecteur colonne a plat pour le parcourir facilement.
    v = etat.flatten()
    lignes = []
    for r in range(3):
        cases = []
        for c in range(3):
     # int() convertit la valeur numpy en entier Python ordinaire,
     # pour qu'elle s'affiche proprement.
            valeur = int(v[r * 3 + c])
     # La case vide est affichee avec un tiret bas.
            cases.append('_' if valeur == 0 else str(valeur))
        lignes.append(' '.join(cases))
    return '\n'.join(lignes)