# Jeu de la vie

[![Tests](https://github.com/yaelpn/git-evaluation-jeu-de-la-vie_groupe8/actions/workflows/tests.yml/badge.svg)](https://github.com/yaelpn/git-evaluation-jeu-de-la-vie_groupe8/actions/runs/45250548935)

Implémentation en Python du [jeu de la vie de Conway](https://fr.wikipedia.org/wiki/Jeu_de_la_vie). Le programme `main.py` calcule l'évolution d'une grille carrée de cellules vivantes (`1`) et mortes (`0`), à partir d'une grille aléatoire ou d'une grille lue sur l'entrée standard, avec des bords fixes ou périodiques (tore). Il produit une image PNG par génération ou une sortie texte.

Projet réalisé par le groupe 8 pour le module outils de développement logiciel.

## Installation

Prérequis : Python 3 et Git. Pour générer les vidéos : `ffmpeg` et Gource. Aucune bibliothèque Python externe n'est nécessaire pour lancer `main.py`.

Récupérer le projet :

```bash
git clone https://github.com/yaelpn/git-evaluation-jeu-de-la-vie_groupe-8.git
cd git-evaluation-jeu-de-la-vie_groupe-8
```

Ubuntu / Debian :

```bash
sudo apt update
sudo apt install python3 git gource ffmpeg
```

macOS (avec [Homebrew](https://brew.sh/)) :

```bash
brew install gource ffmpeg
```

Windows : installer [WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install) (distribution Ubuntu), puis exécuter les commandes Ubuntu ci-dessus dans le terminal WSL. Les disques Windows sont accessibles dans `/mnt`, par exemple `cd /mnt/c/Users/Alice/projet`.

Vérification des outils :

```bash
python3 --version
gource --version
ffmpeg -version
```

## Exécution

Le programme s'exécute depuis la racine du dépôt :

```bash
python3 main.py
```

**Sans option** : 21 images dans `outputs`, de `grid_0000.png` à `grid_0020.png`.

```bash
$ python3 main.py
Generation of 21 images in directory outputs
$ echo $?
0
```

**Grille aléatoire de 50 cellules par côté, graine 4200, 200 itérations** : 201 images.

```bash
$ python3 main.py -n 50 -m 200 -s 4200
Generation of 201 images in directory outputs
```

**Grille lue sur l'entrée standard, bords fixes** (sortie texte) :

```bash
$ cat tests/matrix3/input.txt | python3 main.py -m 1 -t text
iteration: 1
0 1 0
0 0 1
0 1 0
```

**Grille lue sur l'entrée standard, bords périodiques (tore)** :

```bash
$ cat tests/matrix3/input.txt | python3 main.py -m 1 -p -t text
iteration: 1
0 0 0
0 0 0
0 0 0
```

### Format d'une grille en entrée

La première ligne contient la taille de la grille, suivie des lignes de la matrice, dont les cellules sont séparées par des espaces :

```text
3
1 0 1
0 0 1
1 0 1
```

Lorsqu'une grille est fournie sur l'entrée standard, elle remplace la grille aléatoire : les options `--nb_cells` et `--seed` n'ont alors pas d'effet.

### Erreurs

En cas d'entrée invalide (grille vide, non carrée, taille non positive, cellule différente de `0` ou `1`, itération négative, type de sortie inconnu), le programme écrit un message explicite sur la sortie d'erreur (`STDERR`) et se termine avec un code de sortie différent de `0` :

```bash
$ printf '2\n1 2\n0 1\n' | python3 main.py -t text
Erreur : chaque cellule doit valoir 0 ou 1
```

### Tests

Les deux scripts fournis se lancent depuis la racine du dépôt :

```bash
sh check_script_options.sh
sh check_tests.sh
```

### Intégration continue

Un workflow GitHub Actions ([`.github/workflows/tests.yml`](.github/workflows/tests.yml)) exécute automatiquement ces deux scripts sous Linux avec Python 3, à chaque `push` et à chaque *Pull Request*. Il échoue si l'un des scripts se termine avec un code de sortie différent de `0`.

Exécution réussie des deux scripts : [voir l'exécution dans l'onglet Actions](https://github.com/yaelpn/git-evaluation-jeu-de-la-vie_groupe8/actions/runs/45250548935).

## Arguments

| Option courte | Option longue | Description | Valeur par défaut |
|---|---|---|---|
| `-n N` | `--nb_cells N` | nombre de cellules par côté pour une grille aléatoire | `10` |
| `-m N` | `--max_iterations N` | numéro de la dernière itération à calculer | `20` |
| `-s N` | `--seed N` | graine du générateur de nombres aléatoires | `42` |
| `-o DOSSIER` | `--output_directory DOSSIER` | dossier dans lequel écrire les images | `outputs` |
| `-t TYPE` | `--output_type TYPE` | type de sortie : `image` ou `text` | `image` |
| `-p` | `--periodic` | active les conditions aux limites périodiques (tore) | désactivée |
| `-h` | `--help` | affiche l'aide du programme | — |

La génération initiale porte le numéro `0` : avec `-m 20`, la simulation comporte 21 générations, de `0` à `20` incluses.

Avec `-t text`, aucune image n'est écrite : seule la dernière itération est affichée, après la ligne `iteration: N`.

## Vidéos

- **Simulation du jeu de la vie** : [https://www.youtube.com/watch?v=pammKAnzXJY](https://www.youtube.com/watch?v=pammKAnzXJY)
  - Graine utilisée : `4200`
  - Commandes exactes de génération des images et de la vidéo :

    ```bash
    mkdir -p outputs/video-seed-4200
    python3 main.py --nb_cells 50 --max_iterations 2000 --seed 4200 \
      --output_type image --output_directory outputs/video-seed-4200
    ffmpeg -y -framerate 20 -start_number 0 \
      -i outputs/video-seed-4200/grid_%04d.png -frames:v 2001 \
      -c:v libx264 -pix_fmt yuv420p -movflags +faststart \
      outputs/video-seed-4200/game-of-life.mp4
    ```

- **Historique du dépôt (Gource)** : [https://www.youtube.com/watch?v=Vl-trYr61zo](https://www.youtube.com/watch?v=Vl-trYr61zo)

  ```bash
  gource -s 2 -r 60 --file-font-size 8 \
    --title 'Jeu de la vie' --filename-time 2 \
    --stop-at-end --hide date,usernames -o - | \
  ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - \
    -vcodec libx264 -preset medium -pix_fmt yuv420p \
    -crf 18 -threads 0 -bf 0 gource.mp4
  ```

Les images et les vidéos générées ne sont pas versionnées dans Git.

## Auteurs

- HERINIRINASOA Sariaka, 44006654
- PANON Yaël, 45004205
- SAID Darsia, 45001901
- VONJY Zazirka, 45007336

## Liens utiles

- [Workshop 3 : rebase et historique final](https://github.com/frozar/git-workshop-3) : décrit l'organisation Git attendue pour ce projet,
- [Jeu de la vie](https://fr.wikipedia.org/wiki/Jeu_de_la_vie) : présentation des règles du jeu de Conway,
- [Documentation argparse](https://docs.python.org/fr/3/library/argparse.html) : analyse des arguments d'un script Python,
- [Documentation random](https://docs.python.org/fr/3/library/random.html) : génération de grilles aléatoires reproductibles,
- [Pipeline (Unix)](https://en.wikipedia.org/wiki/Pipeline_(Unix)) : description du pipe,
- [Installation de WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install) : procédure officielle pour Windows,
- [Documentation ffmpeg](https://ffmpeg.org/documentation.html) : installation et utilisation de `ffmpeg`,
- [Site officiel de Gource](https://gource.io/) : présentation et téléchargement de Gource,
- [Documentation GitHub Actions](https://docs.github.com/fr/actions) : création et exécution d'un workflow d'intégration continue,
- [Documentation officielle de git rebase](https://git-scm.com/book/fr/v2/Les-branches-avec-Git-Rebaser-Rebasing) : fonctionnement du *rebase*.