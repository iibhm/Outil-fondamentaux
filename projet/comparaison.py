import random
import time

from skyscrapers import (
    grille_aleatoire,
    indices_de,
    grille_valide,
    force_brute,
    retour_sur_trace,
    propagation,
)


def chronometrer(methode, indices):
    debut = time.perf_counter()
    grille, essais = methode(indices)
    return grille, essais, time.perf_counter() - debut


def brute_limitee(indices):
    return force_brute(indices, 400000)


def tester(nom, methode, n, nb_grilles):
    total_temps = 0.0
    total_essais = 0
    abandons = 0
    faux = 0
    s = 0
    while s < nb_grilles:
        random.seed(1000 * n + s)
        indices = indices_de(grille_aleatoire(n))
        grille, essais, duree = chronometrer(methode, indices)
        total_temps += duree
        total_essais += essais
        if grille is None:
            abandons += 1
        elif not grille_valide(grille, indices):
            faux += 1
        s += 1
    print(f"n = {n} | {nom:<17} | essais moyens {total_essais / nb_grilles:>10.0f} | "
          f"temps moyen {total_temps / nb_grilles:>8.4f} s | abandons {abandons}/{nb_grilles} | faux {faux}")


if __name__ == "__main__":
    nb_grilles = 10
    tailles = [4, 5, 6, 7]
    i = 0
    while i < len(tailles):
        n = tailles[i]
        tester("force brute", brute_limitee, n, nb_grilles if n == 4 else 3)
        if n <= 6:
            tester("retour sur trace", retour_sur_trace, n, nb_grilles)
        tester("propagation", propagation, n, nb_grilles)
        print()
        i += 1
