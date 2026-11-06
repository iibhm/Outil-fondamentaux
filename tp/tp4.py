import random
import time
from fractions import Fraction


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


def produit(A, B):
    n, p = len(A), len(A[0])
    if len(B) != p:
        raise ValueError("dimensions incompatibles")
    q = len(B[0])
    C = []
    i = 0
    while i < n:
        C.append([0] * q)
        i += 1
    i = 0
    while i < n:
        j = 0
        while j < q:
            total = 0
            k = 0
            while k < p:
                total += A[i][k] * B[k][j]
                k += 1
            C[i][j] = total
            j += 1
        i += 1
    return C


def matrice_aleatoire(n):
    M = []
    i = 0
    while i < n:
        ligne = []
        j = 0
        while j < n:
            ligne.append(random.random())
            j += 1
        M.append(ligne)
        i += 1
    return M


def resoudre(A, b, eps=1e-14):
    n = len(A)
    M = []
    i = 0
    while i < n:
        M.append(list(A[i]) + [b[i]])
        i += 1
    k = 0
    while k < n:
        meilleure = k
        i = k + 1
        while i < n:
            if abs(M[i][k]) > abs(M[meilleure][k]):
                meilleure = i
            i += 1
        if abs(M[meilleure][k]) <= eps:
            raise ValueError("système singulier ou mal posé")
        M[k], M[meilleure] = M[meilleure], M[k]
        i = k + 1
        while i < n:
            facteur = M[i][k] / M[k][k]
            j = k
            while j <= n:
                M[i][j] -= facteur * M[k][j]
                j += 1
            i += 1
        k += 1
    x = [0.0] * n
    i = n - 1
    while i >= 0:
        total = M[i][n]
        j = i + 1
        while j < n:
            total -= M[i][j] * x[j]
            j += 1
        x[i] = total / M[i][i]
        i -= 1
    return x


def multiplier_vecteur(A, x):
    res = []
    i = 0
    while i < len(A):
        total = 0
        j = 0
        while j < len(x):
            total += A[i][j] * x[j]
            j += 1
        res.append(total)
        i += 1
    return res


def determinant(A):
    n = len(A)
    M = []
    i = 0
    while i < n:
        M.append(list(A[i]))
        i += 1
    det = 1.0
    k = 0
    while k < n:
        meilleure = k
        i = k + 1
        while i < n:
            if abs(M[i][k]) > abs(M[meilleure][k]):
                meilleure = i
            i += 1
        if abs(M[meilleure][k]) < 1e-14:
            return 0.0
        if meilleure != k:
            M[k], M[meilleure] = M[meilleure], M[k]
            det = -det
        det *= M[k][k]
        i = k + 1
        while i < n:
            facteur = M[i][k] / M[k][k]
            j = k
            while j < n:
                M[i][j] -= facteur * M[k][j]
                j += 1
            i += 1
        k += 1
    return det


def hilbert_exacte(n):
    H = []
    i = 0
    while i < n:
        ligne = []
        j = 0
        while j < n:
            ligne.append(Fraction(1, i + j + 1))
            j += 1
        H.append(ligne)
        i += 1
    return H


def somme_des_lignes(M):
    b = []
    i = 0
    while i < len(M):
        total = 0
        j = 0
        while j < len(M[i]):
            total += M[i][j]
            j += 1
        b.append(total)
        i += 1
    return b


A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
b = [2, -1, 8]

print(transposee([[1, 2, 3], [4, 5, 6]]))
print(produit(A, [[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == A)
print(produit([[1, 2], [3, 4]], [[0, 1], [1, 0]]))

random.seed(42)
tailles = [40, 80]
i = 0
while i < len(tailles):
    n = tailles[i]
    M1 = matrice_aleatoire(n)
    M2 = matrice_aleatoire(n)
    debut = time.perf_counter()
    produit(M1, M2)
    print(n, time.perf_counter() - debut)
    i += 1

x = resoudre(A, b)
print(x, multiplier_vecteur(A, x))
print(determinant(A), determinant([[1, 2], [2, 4]]))

H = hilbert_exacte(12)
b_exact = somme_des_lignes(H)
try:
    resoudre(H, b_exact)
except ValueError as erreur:
    print("premier essai :", erreur)
x_exact = resoudre(H, b_exact, eps=0)
ok = True
i = 0
while i < len(x_exact):
    if x_exact[i] != 1:
        ok = False
    i += 1
print(x_exact, ok)
