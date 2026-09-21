# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203) et Adama A Balde (BALA27070105)

# ce fichier contient les outils partages par les trois algos. il ne contient aucun algo
# il contient seulement la structure d'un noeud, la reconstruction du chemin ,
# et la collecte des mesures. le fait de les ecrire une seule fois garantit que BFS ,
# dfs et iddfs sont mesures exactement de la meme facon, ce qui rend leur comparaison juste.

# le noeud de recherche
class Noeud:
    # Represente un etat du puzzle dans l'arbre de recherche.
    # un etat seul ne suffit pas : quand l'algorithme trouve l'objectif, il doit
    # pouvoir retrouver comment il y est arrive. Chaque noeud garde donc aussi
    # une reference vers son parent et l'action qui a permis de l'atteindre.
    # En remontant les parents, on retrouve le chemin complet.

    # __slots__ fixe la liste des attributs d'un noeud. Sans cette ligne,
    # chaque noeud transporterait un dictionnaire interne. Comme certaines
    # recherches creent plusieurs millions de noeuds, cela economise beaucoup
    # de memoire.

    __slots__ = ('etat', 'parent', 'action', 'profondeur')

    def __init__(self, etat, parent=None, action=None):
        # Le vecteur colonne qui decrit la grille.
        self.etat = etat
        # Le noeud precedent dans le chemin ; None pour l'etat initial.
        self.parent = parent
        # Le mouvement qui a mene du parent a ce noeud ("haut", "bas", ...).
        self.action = action
        # Le nombre de coups depuis l'etat initial. La racine est a 0, et
        # chaque enfant est un coup plus loin que son parent.
        self.profondeur = 0 if parent is None else parent.profondeur + 1

# Reconstruction du chemin

def remonter_chemin(noeud):
    # Retourne la liste des actions qui menent de l'etat initial a ce noeud.
    # On part du noeud objectif et on remonte de parent en parent jusqu'a la
    # racine. Les actions sont donc recuperees de la fin vers le debut, et il
    # faut inverser la liste a la fin pour les avoir dans le bon ordre.
    actions = []
    # La racine n'a pas de parent : c'est la condition d'arret. Elle n'a pas
    # non plus d'action, donc elle n'ajoute rien a la liste.
    while noeud.parent is not None:
        actions.append(noeud.action)
        noeud = noeud.parent

    # On remet les actions dans l'ordre chronologique.
    actions.reverse()
    return actions

# Collecte des mesures demandees  par l'enonce.

class Statistiques:
    # Regroupe les mesures prises pendant une execution d'un algorithme.
    # L'enonce demande trois informations : la taille de la frontiere a chaque
    # iteration, le nombre total d'etats explores et le temps d'execution.

    def __init__(self):
        # Une valeur par iteration de la boucle de recherche.
        self.tailles_frontiere = []
        # Le compteur total d'etats explores.
        self.etats_explores = 0
        # Le temps d'execution, rempli par l'algorithme a la fin.
        self.temps = 0.0

    def enregistrer_iteration(self, taille_frontiere):
        # Enregistre une iteration de la boucle de recherche.
        # Une iteration correspond a un etat retire de la frontiere puis traite,
        # c'est-a-dire a un etat explore. Les deux mesures sont donc mises a
        # jour au meme endroit : on ne peut pas oublier l'une sans l'autre, et
        # les trois algorithmes les comptent de la meme maniere.

        self.tailles_frontiere.append(taille_frontiere)
        self.etats_explores += 1