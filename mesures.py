# Laboratoire 1 - 6GEI608 Intelligence artificielle
# Theme : algorithme de resolution du 8-puzzle
# Auteurs : Diallo Ibrahima (DIAI01100203) et Adama A Balde (BALA27070105)

# ce fichier ecrit les fichiers d'evaluation demandes par lenonce
# il est separe des algorithmes pour que ceux la ne soccupent que de la recherche
# et pour que le format des fichiers soit defini a un seul endroiit .
import os

# Dossier dans lequel tous les fichiers de mesures sont ecrits.
DOSSIER_RESULTATS = "resultats"


def nom_fichier(algorithme, entree, execution):
    # Construit le nom du fichier de mesures d'une execution.
    # Le nom contient l'algorithme, l'entree et le numero de l'execution, par
    # exemple BFS_Ex1-1_exec01.txt. Le numero est ecrit sur deux chiffres
    # (01, 02, ..., 10) pour que les fichiers restent dans le bon ordre quand
    # on les trie par nom.

    return f"{algorithme}_{entree}_exec{execution:02d}.txt"


def ecrire(stats, algorithme, entree, execution, dossier=DOSSIER_RESULTATS):
    #Ecrit un fichier de mesures pour une execution.

    #Format :
      # une ligne par iteration : numero_iteration \t taille_de_frontiere
      # avant-derniere ligne    : nombre global d'etats explores
      # derniere ligne          : temps d'execution

    # On cree le dossier s'il n'existe pas encore ; s'il existe deja, cette
    # ligne ne fait rien.
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom_fichier(algorithme, entree, execution))

    # newline="\n" impose des fins de ligne simples. Sous Windows, Python
    # ecrirait sinon des fins de ligne "\r\n", qui ajoutent un caractere
    # invisible a chaque ligne.
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
    # Une ligne par iteration : le numero, une tabulation, puis la taille
    # de la frontiere. La numerotation commence a 1, comme dans l'enonce.
        for numero, taille in enumerate(stats.tailles_frontiere, start=1):
            f.write(f"{numero}\t{taille}\n")

    # Avant-derniere ligne : le nombre total d'etats explores.
        f.write(f"{stats.etats_explores}\n")

    # Derniere ligne : le temps d'execution en secondes. On garde six
    # decimales, car certaines recherches durent moins d'un millieme de
    # seconde et seraient sinon affichees comme 0.
        f.write(f"{stats.temps:.6f}\n")

    return chemin