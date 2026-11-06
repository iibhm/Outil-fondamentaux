# Outils fondamentaux (R1.07) : dépôt de rendu

Étudiant : Ibrahim SAOULI, BUT Informatique 1re année, IUT Nord Franche-Comté, groupe de TP C2. Travail individuel.

## Contenu

- `tp/` : mes solutions aux TP, `tp1.py` à `tp5.py`. Le TP6 (géométrie du plan) n'est pas traité.
- `projet/` : mon projet personnel, un solveur de Skyscrapers (`skyscrapers.py`) et une comparaison chronométrée de trois méthodes (`comparaison.py`).

Tout le code est écrit avec des boucles `while` uniquement, sans `for`.

## Lancer

```
python3 tp/tp1.py            (idem pour tp2 à tp5, chaque fichier teste ses fonctions en bas)
python3 projet/skyscrapers.py
cd projet && python3 comparaison.py
```

`comparaison.py` prend environ une minute. Python 3 suffit, aucune bibliothèque à installer.

## Projet : un solveur de Skyscrapers

**Le jeu.** Une grille n × n doit être remplie avec les chiffres de 1 à n : chaque chiffre apparaît une seule fois par ligne et par colonne, et représente la hauteur d'un immeuble. Les nombres autour de la grille indiquent combien d'immeubles on voit depuis ce côté, un immeuble haut cachant les plus bas derrière lui. Un indice 4 sur une grille 4 × 4 force donc la ligne à `1 2 3 4`.

**La question.** Trois méthodes qui donnent la même solution ont-elles le même coût, et que se passe-t-il quand n grandit ? C'est la question du module : combien de temps, avec quel effort.

**Les trois méthodes** (`projet/skyscrapers.py`) :

1. **Force brute** (`force_brute`) : essaie toutes les grilles faites de lignes qui sont des permutations, soit (n!)^n grilles, et teste chacune.
2. **Retour sur trace** (`retour_sur_trace`) : ne garde pour chaque ligne que les permutations compatibles avec ses deux indices, pose les lignes une à une et revient en arrière dès qu'un chiffre se répète dans une colonne.
3. **Propagation de contraintes** (`propagation`) : garde pour chaque ligne et chaque colonne la liste des permutations compatibles avec les indices, et élimine celles qui contredisent les valeurs encore possibles dans chaque case, jusqu'à ce que plus rien ne change. Si la grille n'est pas résolue, elle essaie les choix de la ligne la plus restreinte.

Les grilles de test viennent de `grille_aleatoire(n)`, qui construit une grille valide au hasard et en déduit les indices. Les graines sont fixées, donc les résultats sont reproductibles.

## Résultats

Moyennes sur 10 grilles (3 pour la force brute à partir de n = 5), mesurées par `comparaison.py`. La force brute est coupée à 400 000 essais.

| n | Méthode | Essais moyens | Temps moyen | Abandons |
|---|---|---|---|---|
| 4 | force brute | 196 495 | 0,32 s | 0/10 |
| 4 | retour sur trace | 19 | 0,0001 s | 0/10 |
| 4 | propagation | 2 | 0,0002 s | 0/10 |
| 5 | force brute | 400 000 (limite) | 0,91 s | 3/3 |
| 5 | retour sur trace | 1 960 | 0,0015 s | 0/10 |
| 5 | propagation | 2 | 0,0011 s | 0/10 |
| 6 | force brute | 400 000 (limite) | 1,14 s | 3/3 |
| 6 | retour sur trace | 1 238 632 | 0,73 s | 0/10 |
| 6 | propagation | 4 | 0,0104 s | 0/10 |
| 7 | force brute | 400 000 (limite) | 1,51 s | 3/3 |
| 7 | propagation | 8 | 0,0775 s | 0/10 |

Aucune solution renvoyée n'est fausse : chacune est revérifiée par `grille_valide`.

## Ce qu'on doit observer

- **La force brute devient impossible dès n = 5.** Pour n = 4 il y a 24^4 = 331 776 grilles possibles, et elle en teste environ 196 000 en moyenne. Pour n = 5 il y en a 120^5, soit environ 2,5 × 10^10 : elle abandonne à la limite sur toutes les grilles.
- **Le retour sur trace explose entre n = 5 et n = 6** : de 1 960 à plus d'un million d'essais. L'élagage par les colonnes ne suffit plus quand les listes de lignes candidates grandissent.
- **La propagation reste à quelques nœuds** (2 à 8) parce que les indices éliminent presque tout avant même qu'on fasse un choix.
- **Moins d'essais ne veut pas dire moins de temps.** Pour la propagation, le temps passe de 0,0002 s à 0,0775 s alors que le nombre de nœuds reste petit : chaque nœud coûte beaucoup plus cher, car il recalcule les valeurs possibles de toutes les cases.

## Limites

- Les « essais » n'ont pas la même unité selon la méthode (grilles testées, lignes essayées, nœuds de propagation) : on compare des ordres de grandeur, pas des chiffres exacts.
- Les grilles aléatoires n'ont pas forcément une solution unique. Les solveurs renvoient la première trouvée, qui peut différer de la grille d'origine tout en respectant tous les indices.
- Pour la force brute à partir de n = 5, le temps mesuré est celui de la limite de 400 000 essais, pas celui d'une résolution complète.
- La liste de toutes les permutations occupe n! listes en mémoire, ce qui bloque à n = 9 ou 10. Les temps dépendent de ma machine.

## Ce que j'ai observé et ce qui n'a pas marché

**Pourquoi ce sujet.** Je jouais à ce jeu sans plus me souvenir de son nom, et je me suis demandé si un ordinateur le résoudrait « en force » ou s'il fallait réfléchir comme un humain. Le module répète qu'un programme juste mais trop lent est inutilisable : ce jeu était un bon terrain pour le vérifier.

**Ce qui m'a surpris.**
- Je pensais que la force brute tiendrait au moins jusqu'à 5 × 5. En calculant le nombre de grilles, (n!)^n, on voit que non : 331 776 pour n = 4, mais environ 2,5 × 10^10 pour n = 5, 1,4 × 10^17 pour n = 6 et 8,3 × 10^25 pour n = 7. Passer de 4 à 5 multiplie le travail par 75 000, c'est la même leçon que la version naïve de Fibonacci au TP2.
- Le retour sur trace, qui paraissait « intelligent », s'effondre lui aussi à n = 6 : plus d'un million d'essais, contre 1 960 à n = 5. Un meilleur algorithme repousse le mur, il ne le supprime pas.
- Les indices font presque tout le travail. Sur une ligne de 4, il existe 24 permutations, mais un couple d'indices (gauche, droite) n'en laisse que 1 à 6 : par exemple (1, 4) ou (4, 1) imposent une seule ligne, (2, 2) en laisse 6. C'est pour ça que la propagation n'a besoin que de 2 à 8 nœuds.
- Compter les essais ne suffit pas : la propagation fait très peu d'essais mais chacun coûte de plus en plus cher (0,0002 s à n = 4, 0,08 s à n = 7). Il faut mesurer le temps, pas seulement compter, comme l'exercice sur Horner au TP3 où la prévision était fausse.

**Ce qui n'a pas marché.**
- Ma première mesure coupait la force brute à 200 000 essais : la moitié des grilles 4 × 4 étaient comptées comme des échecs alors qu'il manquait juste du temps. J'ai monté la limite à 400 000 pour que le 4 × 4 passe toujours, et j'ai gardé la limite pour les tailles plus grandes, sinon le programme ne finit jamais.
- Je voulais vérifier que la solution trouvée était la grille d'origine, mais certaines grilles aléatoires ont plusieurs solutions. J'ai donc vérifié les indices de la solution trouvée (avec `grille_valide`) plutôt que de la comparer à l'originale.

**Pour aller plus loin.** Générer des grilles à solution unique (en retirant des indices tant que la solution reste unique), et estimer la croissance du temps de chaque méthode par une régression sur le logarithme des temps, résolue avec le pivot de Gauss du TP4.

## Usage de l'intelligence artificielle

- J'ai utilisé Claude (assistant IA) pour écrire une première version du code des TP et du projet, à partir de mon sujet et de mon style (boucles `while` uniquement, variables `i` puis `j`).
- Ce que j'ai vérifié moi-même :
  - j'ai lancé chaque fichier de `tp/` et comparé les sorties aux « résultats attendus » des énoncés (par exemple `289 3` au TP1, `9592` premiers sous 100 000 au TP2, `[3, -1, 0.5]` pour Gauss au TP4, 312 clés au TP5) ;
  - j'ai vérifié qu'il n'y a aucune boucle `for` dans le code, pour garder mon style ;
  - pour le projet, chaque solution renvoyée est revérifiée par `grille_valide`, et `comparaison.py` compte les solutions fausses (0 sur toutes les mesures) ;
  - j'ai recalculé à la main le nombre de grilles (n!)^n pour comprendre pourquoi la force brute abandonne dès n = 5.
