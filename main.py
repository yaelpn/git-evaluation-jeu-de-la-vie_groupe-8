import random
import sys


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


from lib import write_grid

import argparse


def compte_voisins(grille, x, y):
    voisins = 0
    lignes = len(grille)
    colonnes = len(grille[0])
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i, j) != (x, y) and 0 <= i < lignes and 0 <= j < colonnes:
                voisins += grille[i][j]
    return voisins

def nouvelle_valeur_cellule(etat_actuel, nb_voisins):
    if etat_actuel == 1:
        return 1 if nb_voisins in (2, 3) else 0
    else:
        return 1 if nb_voisins == 3 else 0

def calculer_generation_suivante(grille):
    lignes = len(grille)
    colonnes = len(grille[0])
    nouvelle_grille = [[0 for _ in range(colonnes)] for _ in range(lignes)]
    for i in range(lignes):
        for j in range(colonnes):
            nb_voisins = compte_voisins(grille, i, j)
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
    parser.add_argument("-t", "--output_type", choices=['image','text'], default='image', 
                        help="type de sortie image ou text")
    parser.add_argument("-p", "--periodic", action='store_true', 
                        help="active les conditions aux limites périodiques ") 

    args = parser.parse_args() 

    if args.nb_cells <= 0:
        parser.error("Le nombre de cellules doit être supérieur à 0")
    if args.max_iterations < 0:
        parser.error("Le nombre d'itération ne peut pas être négatif")
    return args

def main():
    nb_cells = 50

    rng = random.Random(4200)

    matrix = [
        [rng.choice([0, 1]) for _ in range(nb_cells)]
        for _ in range(nb_cells)
    ]

    iter = 0
    filename = f"outputs/grid_{iter:04d}.png"
    write_grid(matrix=matrix, filename=filename)

if __name__ == "__main__":
    main()
