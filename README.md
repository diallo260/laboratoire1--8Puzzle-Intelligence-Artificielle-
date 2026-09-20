# Université du Québec à Chicoutimi 

## Laboratoire 1- Algorithmes de recherche sur le 8-puzzle

## Cours 6GEI608- Intelligence artificielle et reconnaissance des formes 

## Travail réalisé par : 
Diallo Ibrahima (DIAI01100203)
Adama A Baldé (BALA27070105) 

## Commande pour exécuter le code : 
python main.py   (exécute les quatre entrées)
python main.py Ex1-1 (exécute seulement la première entrée)

## Organisation des fichiers :
* puzzle.py : ce fichier représente le 8-puzzle, il fait la lecture des fichiers et la génération des voisins.
* recherche.py : outils communs qui fait également la reconstruction du chemin.
* bfs.py, dfs.py, iddfs.py : ces trois fichiers sont les trois algorithmes demandés 
* mesures.py : ce fichier permet d'écrire les fichiers d'évaluation
* main.py : fichier qui permet l'exécution (3 algos x 4 entrées x 10 exécutions)
* entree, résultats et chemins sont des dossiers à la racine du projet. 

Les chemins sont écrits à part parce que ceux du dfs dépassent 60 000 actions.
Un seul fichier par algorithme et par entrée.
Les dix exécutions donnent le même chemin.

## Ce que j'ai compris : 

Dans notre implémentation, nous avons choisi de représenter l’état comme un vecteur de 9 cases et les mouvements comme des matrices de permutation.
J'ai compris quand j'ai réalisé que déplacer la case vide revenait à échanger deux éléments du vecteur.
Un échange s'écrit comme l'identité dont on a interverti deux lignes.
Générer les voisins devient une boucle de multiplication, sans aucune condition ou contrainte à écrire.

Un tableau numpy ne peut pas servir de clé. Mon ensemble d'états visités
plantait avec unhashable type: numpy.ndarray. Numpy interdit cette opération
parce qu'un tableau peut être modifié après coup. La solution était de stocker une
version figée avec tobytes() plutôt que le tableau lui-même.

Le DFS m'a beaucoup surprise. Avec une limite de profondeur de 50, il
explorait 140 145 états sur Ex1-1 et concluait qu'il n'y avait pas de solution,
alors que le BFS en trouvait une en 20 coups. J'ai cru à un bug. En fait, comme il
marque les états visités pour toute l'exécution, il en « brûle » des milliers en
descendant, et ces états deviennent inaccessibles aux autres branches. En testant
d'autres limites, les résultats n'avaient aucune logique : échec à 31, succès à
100, échec à 200.

Sans limite, il trouve bien une solution mais, de 65 971 coups sur un puzzle qui
se résout en 17. Ça m'a fait comprendre concrètement ce que veut dire un algorithme 
non optimal.

Pourquoi dix exécutions, mes résultats étaient identiques à chaque lancement,
et je ne comprenais pas. C'est justement parce que les algorithmes
sont déterministes : seul le temps varie, selon ce que fait la machine. Les dix
exécutions servent à obtenir une moyenne fiable.

## Comparaison des trois algorithmes

Moyennes sur dix exécutions, tirées de `resultats/journal_execution.txt`.

| Entrée | BFS | DFS | IDDFS |
|---|---|---|---|
| Ex1-1 (20 coups) | 20 — 0,665 s | 2 698 — 0,035 s | 20 — 1,491 s |
| Ex1-2 (17 coups) | 17 — 0,167 s | 65 971 — 1,062 s | 17 — 0,417 s |
| Ex1-3 (insoluble) | échec — 2,024 s | échec — 1,903 s | échec — 43,425 s |
| Ex1-4 (28 coups) | 28 — 1,909 s | 64 830 — 1,168 s | 28 — 22,136 s |

- Discussion des résultats : C'est la différence la plus nette. Le BFS et l'IDDFS
trouvent toujours le chemin le plus court. Dans nos trois entrées solubles, le DFS n’a jamais trouvé le chemin optimal.
Sur Ex1-2, 65 971 coups au lieu de 17. Son chemin est valide, mais très mauvais.
Le BFS avance niveau par niveau, donc la première solution qu'il croise est
forcément la plus courte. L'IDDFS obtient le même résultat en cherchant d'abord
en 0 coup, puis 1, puis 2. Le DFS plonge dans la première branche venue.

- Discussion sur la limite : lors de mes essais, j'ai d'abord utilisé un dfs avec une limite de profondeur. 
Avec une limite de 50, la frontière restait très petite, mais l'algorithme pouvait échouer même lorsqu'une solution existait.
Nous avons donc retiré cette limite dans la version finale. Sans limite, le dfs trouve bien les solutions des entrées solubles,
mais sa frontière peut devenir beaucoup plus grande et les chemins obtenus peuvent être très longs.

- Discussion sur le temps : moins tranché que je ne l'imaginais. Le DFS met 0,035 s sur Ex1-1,
il explore seulement 2 775 états avant de trouver l’objectif, ce qui explique son faible temps d’exécution.
Sur Ex1-2 il devient six fois plus lent que le BFS. Le BFS est le plus stable. L'IDDFS est toujours le plus lent, ce qui
est logique puisqu'il recommence à chaque limite : 43 secondes sur Ex1-3, où il
épuise les 31 limites sans jamais trouver.

- Le BFS est le meilleur choix par défaut à cause de sa rapidité et de sa régularité. Sa limite est la mémoire.
L’IDDFS garde généralement une frontière plus petite, mais répète davantage d’explorations, en échange de plus de temps,
ce point est le compromis que je trouve le plus intéressant. Le DFS peut être rapide sur certaines entrées, mais il ne garantit
pas le chemin optimal et ses résultats dépendent fortement de l’ordre d’exploration.