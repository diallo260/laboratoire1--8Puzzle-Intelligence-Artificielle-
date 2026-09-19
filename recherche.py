# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203)


class Noeud:
    """Un etat du puzzle, plus de quoi remonter jusqu'a la racine."""

    __slots__ = ('etat', 'parent', 'action', 'profondeur')

    def __init__(self, etat, parent=None, action=None):
        self.etat = etat
        self.parent = parent
        self.action = action
        self.profondeur = 0 if parent is None else parent.profondeur + 1


def remonter_chemin(noeud):
    """Liste des actions de la racine jusqu'a ce noeud."""
    actions = []
    while noeud.parent is not None:
        actions.append(noeud.action)
        noeud = noeud.parent
    actions.reverse()
    return actions


class Statistiques:
    """Mesures exigees par l'enonce, collectees pendant une execution."""

    def __init__(self):
        self.tailles_frontiere = []   # une entree par iteration
        self.etats_explores = 0
        self.temps = 0.0

    def enregistrer_iteration(self, taille_frontiere):
        self.tailles_frontiere.append(taille_frontiere)
        self.etats_explores += 1