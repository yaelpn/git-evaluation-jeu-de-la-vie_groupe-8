import random
import argparse
import sys
import os

from lib import write_grid


def lire_grille_stdin():
    lignes = [l.split() for l in sys.stdin.read().splitlines() if l.strip()]
    if not lignes:
        raise ValueError("grille vide")
    if len(lignes[0]) != 1 or not lignes[0][0].isdigit():
        raise ValueError("la première ligne doit contenir la taille de la grille")
    taille = int(lignes[0][0])
    if taille <= 0:
        raise ValueError("la taille doit être strictement positive")

    rangees = lignes[1:]
    if len(rangees) != taille or any(len(r) != taille for r in rangees):
        raise ValueError("la grille doit être carrée et correspondre à la taille indiquée")
    if any(c not in ("0", "1") for r in rangees for c in r):
        raise ValueError("chaque cellule doit valoir 0 ou 1")

    return [[int(c) for c in r] for r in rangees]


def Generation_de_grille(lignes, colonnes, seed_val=42, densite=0.5):
    rng = random.Random(seed_val)
    plateau = [1 if rng.random() < densite else 0 for _ in range(colonnes * lignes)]
    return [plateau[i * colonnes:(i + 1) * colonnes] for i in range(lignes)]


def get_cellule(grille, i, j, periodique=False):
    nb_lignes = len(grille)
    nb_cols = len(grille[0])

    if periodique:
        i = i % nb_lignes
        j = j % nb_cols
    else:
        if not (0 <= i < nb_lignes and 0 <= j < nb_cols):
            return 0

    return grille[i][j]


def compte_voisins(grille, x, y, periodique=False):
    voisins = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i, j) != (x, y):
                voisins += get_cellule(grille, i, j, periodique)
    return voisins


def nouvelle_valeur_cellule(etat_actuel, nb_voisins):
    if etat_actuel == 1:
        return 1 if nb_voisins in (2, 3) else 0
    else:
        return 1 if nb_voisins == 3 else 0


def calculer_generation_suivante(grille, periodique=False):
    lignes = len(grille)
    colonnes = len(grille[0])
    nouvelle_grille = [[0 for _ in range(colonnes)] for _ in range(lignes)]
    for i in range(lignes):
        for j in range(colonnes):
            nb_voisins = compte_voisins(grille, i, j, periodique)
            nouvelle_grille[i][j] = nouvelle_valeur_cellule(grille[i][j], nb_voisins)
    return nouvelle_grille


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--nb_cells", type=int, default=10,
                        help="nombre de cellules par côté pour un grille aléatoire")
    parser.add_argument("-m", "--max_iterations", type=int, default=20,
                        help="numéro de la dernière itération à calculer")
    parser.add_argument("-s", "--seed", type=int, default=42,
                        help="graine de générateur de nombres aléatoires")
    parser.add_argument("-o", "--output_directory", type=str, default='outputs',
                        help="dossier dans lequel écrire les images")
    parser.add_argument("-t", "--output_type", choices=['image', 'text'], default='image',
                        help="type de sortie image ou text")
    parser.add_argument("-p", "--periodic", action='store_true',
                        help="active les conditions aux limites périodiques ")

    args = parser.parse_args()

    if args.nb_cells <= 0:
        parser.error("Le nombre de cellules doit être supérieur à 0")
    if args.max_iterations < 0:
        parser.error("Le nombre d'itération ne peut pas être négatif")
    return args


def sortie_image(matrix, iteration, dossier):
    try:
        os.makedirs(dossier, exist_ok=True)
    except OSError as e:
        erreur(f"impossible de créer le dossier '{dossier}' : {e}")
    filename = os.path.join(dossier, f"grid_{iteration:04d}.png")
    write_grid(matrix=matrix, filename=filename)


def sortie_texte(matrix, iteration):
    print(f"iteration: {iteration}")
    for ligne in matrix:
        print(" ".join(str(c) for c in ligne))


def valider_grille(matrix):
    if not isinstance(matrix, list) or len(matrix) == 0:
        raise ValueError("la grille est vide")
    n = len(matrix)
    for i, ligne in enumerate(matrix):
        if not isinstance(ligne, list) or len(ligne) == 0:
            raise ValueError(f"la ligne {i} est vide ou mal formée")
        if len(ligne) != n:
            raise ValueError(
                f"la grille doit être carrée : {n} lignes mais la ligne {i} "
                f"contient {len(ligne)} cellules"
            )
        for j, cellule in enumerate(ligne):
            if type(cellule) is not int or cellule not in (0, 1):
                raise ValueError(
                    f"cellule invalide en ({i}, {j}) : {cellule!r} "
                    "(seuls 0 et 1 sont acceptés)"
                )


def erreur(message):
    print(f"Erreur : {message}", file=sys.stderr)
    sys.exit(1)


def main():
    args = parse_args()

    try:
        if not sys.stdin.isatty():      # grille fournie via STDIN (pipe ou redirection)
            matrix = lire_grille_stdin()
        else:                           # sinon, grille aléatoire
            matrix = Generation_de_grille(args.nb_cells, args.nb_cells, args.seed, 0.5)
        valider_grille(matrix)
    except ValueError as e:
        erreur(e)

    if args.output_type == "image":
        sortie_image(matrix, 0, args.output_directory)
        for iteration in range(1, args.max_iterations + 1):
            matrix = calculer_generation_suivante(matrix, args.periodic)
            sortie_image(matrix, iteration, args.output_directory)
        print(f"Generation of {args.max_iterations + 1} images "
              f"in directory {args.output_directory}")
    else:
        for _ in range(args.max_iterations):
            matrix = calculer_generation_suivante(matrix, args.periodic)
        sortie_texte(matrix, args.max_iterations)


if __name__ == "__main__":
    main()
