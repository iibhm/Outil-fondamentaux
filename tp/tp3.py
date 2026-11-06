import math


def evaluer_naif(P, x):
    total = 0
    i = 0
    while i < len(P):
        total += P[i] * x ** i
        i += 1
    return total


def evaluer(P, x):
    total = 0
    i = len(P) - 1
    while i >= 0:
        total = total * x + P[i]
        i -= 1
    return total


def deriver(P):
    res = []
    i = 1
    while i < len(P):
        res.append(i * P[i])
        i += 1
    return res


def dichotomie(f, a, b, eps=1e-12):
    fa, fb = f(a), f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("f(a) et f(b) doivent avoir des signes opposés")
    while b - a > eps:
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


def newton(P, x0, eps=1e-12, max_iter=100):
    derivee = deriver(P)
    x = float(x0)
    k = 0
    while k < max_iter:
        val = evaluer(P, x)
        pente = evaluer(derivee, x)
        if pente == 0:
            raise ZeroDivisionError("Dérivée nulle, divergence.")
        suivant = x - val / pente
        k += 1
        if abs(suivant - x) <= eps * max(1.0, abs(suivant)):
            return suivant, k
        x = suivant
    raise RuntimeError("pas de convergence en {} tours".format(max_iter))


def newton_trace(P, x0, tours):
    derivee = deriver(P)
    x = float(x0)
    trajet = [x]
    k = 0
    while k < tours:
        pente = evaluer(derivee, x)
        if pente == 0:
            break
        x = x - evaluer(P, x) / pente
        trajet.append(x)
        k += 1
    return trajet


def somme(P, Q):
    n = max(len(P), len(Q))
    res = []
    i = 0
    while i < n:
        p = P[i] if i < len(P) else 0
        q = Q[i] if i < len(Q) else 0
        res.append(p + q)
        i += 1
    return res


def produit_poly(P, Q):
    if len(P) == 0 or len(Q) == 0:
        return []
    res = [0] * (len(P) + len(Q) - 1)
    i = 0
    while i < len(P):
        j = 0
        while j < len(Q):
            res[i + j] += P[i] * Q[j]
            j += 1
        i += 1
    return res


def derivee_avant(f, x, h):
    return (f(x + h) - f(x)) / h


def derivee_centree(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


def rectangles(f, a, b, n):
    h = (b - a) / n
    total = 0
    i = 0
    while i < n:
        total += f(a + i * h)
        i += 1
    return h * total


def trapezes(f, a, b, n):
    h = (b - a) / n
    total = 0
    i = 1
    while i < n:
        total += f(a + i * h)
        i += 1
    return h * ((f(a) + f(b)) / 2 + total)


def simpson(f, a, b, n):
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    impairs = 0
    i = 1
    while i < n:
        impairs += f(a + i * h)
        i += 2
    pairs = 0
    j = 2
    while j < n:
        pairs += f(a + j * h)
        j += 2
    return h / 3 * (f(a) + f(b) + 4 * impairs + 2 * pairs)


def carre(x):
    return x * x


def carre_moins_deux(x):
    return x * x - 2


def pour_pi(x):
    return 4 / (1 + x * x)


P = [2, 3, 0, 5]
print(evaluer_naif(P, 2), evaluer(P, 2), evaluer(P, 0), evaluer([], 5))
print(deriver(P), deriver([7]))

racine = dichotomie(carre_moins_deux, 0, 2)
print(racine, abs(racine - 2 ** 0.5) < 1e-9)
Q = [-5, -2, 0, 1]
departs = [2, 1, 0]
i = 0
while i < len(departs):
    racine, tours = newton(Q, departs[i])
    print(departs[i], tours, racine)
    i += 1
R = [2, -2, 0, 1]
print(newton_trace(R, 0, 8))
try:
    print(newton(R, 0))
except RuntimeError as erreur:
    print("échec :", erreur)

print(somme([1, 2], [0, 0, 3]))
print(produit_poly([1, 1], [1, 1]), produit_poly([-1, 1], [1, 1]))
binome = [1]
i = 0
while i < 10:
    binome = produit_poly(binome, [1, 1])
    i += 1
print(binome)

pas = [1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12]
i = 0
while i < len(pas):
    h = pas[i]
    print(h, abs(derivee_avant(math.sin, 1.0, h) - math.cos(1.0)), abs(derivee_centree(math.sin, 1.0, h) - math.cos(1.0)))
    i += 1

nombres = [10, 100, 1000]
i = 0
while i < len(nombres):
    n = nombres[i]
    print(n, abs(rectangles(carre, 0, 1, n) - 1 / 3), abs(trapezes(carre, 0, 1, n) - 1 / 3), abs(simpson(carre, 0, 1, n) - 1 / 3))
    i += 1
print(abs(trapezes(pour_pi, 0, 1, 1000) - math.pi), abs(simpson(pour_pi, 0, 1, 1000) - math.pi))
