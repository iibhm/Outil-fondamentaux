import random


def transposee(A):
    x = len(A)
    y = len(A[0])
    res = []
    j = 0
    while j < y:
        ligne = []
        i = 0
        while i < x:
            ligne.append(A[i][j])
            i += 1
        res.append(ligne)
        j += 1
    return res


def permutations(n):
    res = [[]]
    k = 0
    while k < n:
        nouveau = []
        i = 0
        while i < len(res):
            v = 1
            while v <= n:
                if v not in res[i]:
                    nouveau.append(res[i] + [v])
                v += 1
            i += 1
        res = nouveau
        k += 1
    return res


def visibles(ligne):
    total = 0
    max_vu = 0
    i = 0
    while i < len(ligne):
        if ligne[i] > max_vu:
            total += 1
            max_vu = ligne[i]
        i += 1
    return total


def joindre(liste):
    res = ""
    i = 0
    while i < len(liste):
        if i > 0:
            res += " "
        res += str(liste[i])
        i += 1
    return res


def afficher(grille, indices):
    haut, bas, gauche, droite = indices
    if grille is None:
        print("aucune solution")
        return
    print("    " + joindre(haut))
    i = 0
    while i < len(grille):
        print(str(gauche[i]) + "   " + joindre(grille[i]) + "   " + str(droite[i]))
        i += 1
    print("    " + joindre(bas))


def indices_de(grille):
    n = len(grille)
    colonnes = transposee(grille)
    haut, bas, gauche, droite = [], [], [], []
    i = 0
    while i < n:
        haut.append(visibles(colonnes[i]))
        bas.append(visibles(colonnes[i][::-1]))
        gauche.append(visibles(grille[i]))
        droite.append(visibles(grille[i][::-1]))
        i += 1
    return haut, bas, gauche, droite


def grille_valide(grille, indices):
    haut, bas, gauche, droite = indices
    n = len(grille)
    colonnes = transposee(grille)
    j = 0
    while j < n:
        if len(set(colonnes[j])) != n:
            return False
        j += 1
    i = 0
    while i < n:
        if visibles(grille[i]) != gauche[i] or visibles(grille[i][::-1]) != droite[i]:
            return False
        if visibles(colonnes[i]) != haut[i] or visibles(colonnes[i][::-1]) != bas[i]:
            return False
        i += 1
    return True


def compatible(grille, ligne):
    i = 0
    while i < len(grille):
        j = 0
        while j < len(ligne):
            if grille[i][j] == ligne[j]:
                return False
            j += 1
        i += 1
    return True


def completer(grille, perms, n):
    if len(grille) == n:
        return True
    k = 0
    while k < len(perms):
        if compatible(grille, perms[k]):
            grille.append(perms[k])
            if completer(grille, perms, n):
                return True
            grille.pop()
        k += 1
    return False


def grille_aleatoire(n):
    perms = permutations(n)
    random.shuffle(perms)
    grille = []
    completer(grille, perms, n)
    return grille


def force_brute(indices, limite=10 ** 7):
    n = len(indices[0])
    perms = permutations(n)
    m = len(perms)
    choix = [0] * n
    essais = 0
    fini = False
    while not fini and essais < limite:
        grille = []
        i = 0
        while i < n:
            grille.append(perms[choix[i]])
            i += 1
        essais += 1
        if grille_valide(grille, indices):
            return grille, essais
        i = n - 1
        while i >= 0 and choix[i] == m - 1:
            choix[i] = 0
            i -= 1
        if i < 0:
            fini = True
        else:
            choix[i] += 1
    return None, essais


def candidats(debut, fin, perms):
    res = []
    i = 0
    while i < len(debut):
        liste = []
        k = 0
        while k < len(perms):
            if visibles(perms[k]) == debut[i] and visibles(perms[k][::-1]) == fin[i]:
                liste.append(perms[k])
            k += 1
        res.append(liste)
        i += 1
    return res


def placer(grille, i, lignes, indices, compteur):
    if i == len(lignes):
        return grille_valide(grille, indices)
    k = 0
    while k < len(lignes[i]):
        compteur[0] += 1
        if compatible(grille, lignes[i][k]):
            grille.append(lignes[i][k])
            if placer(grille, i + 1, lignes, indices, compteur):
                return True
            grille.pop()
        k += 1
    return False


def retour_sur_trace(indices):
    haut, bas, gauche, droite = indices
    perms = permutations(len(haut))
    lignes = candidats(gauche, droite, perms)
    grille = []
    compteur = [0]
    if placer(grille, 0, lignes, indices, compteur):
        return grille, compteur[0]
    return None, compteur[0]


def copier(listes):
    res = []
    i = 0
    while i < len(listes):
        res.append(list(listes[i]))
        i += 1
    return res


def valeurs_possibles(lignes, colonnes, i, j):
    vu_ligne = set()
    k = 0
    while k < len(lignes[i]):
        vu_ligne.add(lignes[i][k][j])
        k += 1
    vu_colonne = set()
    k = 0
    while k < len(colonnes[j]):
        vu_colonne.add(colonnes[j][k][i])
        k += 1
    return vu_ligne & vu_colonne


def ligne_ok(p, i, poss):
    j = 0
    while j < len(p):
        if p[j] not in poss[i][j]:
            return False
        j += 1
    return True


def colonne_ok(q, j, poss):
    i = 0
    while i < len(q):
        if q[i] not in poss[i][j]:
            return False
        i += 1
    return True


def propager(lignes, colonnes):
    n = len(lignes)
    change = True
    while change:
        change = False
        poss = []
        i = 0
        while i < n:
            poss.append([])
            j = 0
            while j < n:
                poss[i].append(valeurs_possibles(lignes, colonnes, i, j))
                j += 1
            i += 1
        i = 0
        while i < n:
            gardees = []
            k = 0
            while k < len(lignes[i]):
                if ligne_ok(lignes[i][k], i, poss):
                    gardees.append(lignes[i][k])
                k += 1
            if len(gardees) != len(lignes[i]):
                change = True
            lignes[i] = gardees
            if len(gardees) == 0:
                return False
            i += 1
        j = 0
        while j < n:
            gardees = []
            k = 0
            while k < len(colonnes[j]):
                if colonne_ok(colonnes[j][k], j, poss):
                    gardees.append(colonnes[j][k])
                k += 1
            if len(gardees) != len(colonnes[j]):
                change = True
            colonnes[j] = gardees
            if len(gardees) == 0:
                return False
            j += 1
    return True


def resoudre_propagation(lignes, colonnes, indices, compteur):
    compteur[0] += 1
    if not propager(lignes, colonnes):
        return None
    n = len(lignes)
    meilleure = -1
    i = 0
    while i < n:
        if len(lignes[i]) > 1 and (meilleure == -1 or len(lignes[i]) < len(lignes[meilleure])):
            meilleure = i
        i += 1
    if meilleure == -1:
        grille = []
        i = 0
        while i < n:
            grille.append(lignes[i][0])
            i += 1
        if grille_valide(grille, indices):
            return grille
        return None
    k = 0
    while k < len(lignes[meilleure]):
        copie_lignes = copier(lignes)
        copie_colonnes = copier(colonnes)
        copie_lignes[meilleure] = [lignes[meilleure][k]]
        res = resoudre_propagation(copie_lignes, copie_colonnes, indices, compteur)
        if res is not None:
            return res
        k += 1
    return None


def propagation(indices):
    haut, bas, gauche, droite = indices
    perms = permutations(len(haut))
    lignes = candidats(gauche, droite, perms)
    colonnes = candidats(haut, bas, perms)
    compteur = [0]
    grille = resoudre_propagation(lignes, colonnes, indices, compteur)
    return grille, compteur[0]


if __name__ == "__main__":
    random.seed(7)
    solution = grille_aleatoire(4)
    indices = indices_de(solution)
    print("grille cachée :")
    afficher(solution, indices)
    print()
    grille, essais = force_brute(indices)
    print("force brute :", essais, "grilles testées")
    afficher(grille, indices)
    grille, essais = retour_sur_trace(indices)
    print("retour sur trace :", essais, "lignes essayées")
    afficher(grille, indices)
    grille, essais = propagation(indices)
    print("propagation :", essais, "noeuds")
    afficher(grille, indices)
