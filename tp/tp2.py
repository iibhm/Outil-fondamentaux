import time


def diviseurs(n):
    res = []
    i = 1
    while i <= n:
        if n % i == 0:
            res.append(i)
        i += 1
    return res


def pgcd_naif(a, b):
    meilleur = 1
    i = 1
    while i <= min(a, b):
        if a % i == 0 and b % i == 0:
            meilleur = i
        i += 1
    return meilleur


def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def est_premier_naif(n):
    if n < 2:
        return False
    i = 2
    while i < n:
        if n % i == 0:
            return False
        i += 1
    return True


def est_premier(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def duree(fonction, argument):
    debut = time.perf_counter()
    fonction(argument)
    return time.perf_counter() - debut


def crible(limite):
    est_prem = [True] * (limite + 1)
    est_prem[0] = False
    if limite >= 1:
        est_prem[1] = False
    d = 2
    while d * d <= limite:
        if est_prem[d]:
            multiple = d * d
            while multiple <= limite:
                est_prem[multiple] = False
                multiple += d
        d += 1
    res = []
    i = 0
    while i <= limite:
        if est_prem[i]:
            res.append(i)
        i += 1
    return res


def facteurs(n):
    res = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            res.append(d)
            n //= d
        d += 1
    if n > 1:
        res.append(n)
    return res


def fibonacci_recursif(n):
    if n < 2:
        return n
    return fibonacci_recursif(n - 1) + fibonacci_recursif(n - 2)


appels = {}


def fibonacci_compte(n):
    appels[n] = appels.get(n, 0) + 1
    if n < 2:
        return n
    return fibonacci_compte(n - 1) + fibonacci_compte(n - 2)


def fibonacci(n):
    precedent, courant = 0, 1
    i = 0
    while i < n:
        precedent, courant = courant, precedent + courant
        i += 1
    return precedent


def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    g, u, v = euclide_etendu(b, a % b)
    return g, v, u - (a // b) * v


def puissance_mod_naive(a, e, n):
    res = 1
    i = 0
    while i < e:
        res = res * a % n
        i += 1
    return res


def puissance_mod(a, e, n):
    res = 1
    a = a % n
    while e > 0:
        if e % 2 == 1:
            res = res * a % n
        a = a * a % n
        e //= 2
    return res


print(diviseurs(28), diviseurs(97))
print(pgcd_naif(1071, 462), pgcd(1071, 462))
print(est_premier_naif(97), est_premier_naif(91))
print(est_premier(97), est_premier(91), est_premier(2), est_premier(1), est_premier(-7))

tailles = [10007, 100003, 1000003]
i = 0
while i < len(tailles):
    n = tailles[i]
    print(n, duree(est_premier_naif, n), duree(est_premier, n))
    i += 1

p = crible(100)
print(p, len(p))
print(len(crible(100000)))

f = facteurs(360)
produit = 1
i = 0
while i < len(f):
    produit *= f[i]
    i += 1
print(f, produit, facteurs(14))

liste = []
i = 0
while i < 15:
    liste.append(fibonacci_recursif(i))
    i += 1
print(liste)
print(duree(fibonacci_recursif, 25))
print(fibonacci_compte(25), appels[1])
print(fibonacci(30), len(str(fibonacci(10000))))

g, u, v = euclide_etendu(1071, 462)
print(g, u, v, 1071 * u + 462 * v == g)
print(euclide_etendu(5, 26))
print(puissance_mod(7, 10 ** 6, 1000003), puissance_mod_naive(7, 10 ** 6, 1000003), pow(7, 10 ** 6, 1000003))
