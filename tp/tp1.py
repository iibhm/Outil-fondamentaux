import math
from fractions import Fraction


def division_euclidienne(n, d):
    return n // d, n % d


def dernier_chiffre(n):
    return n % 10, n // 10


def somme_dixiemes(n):
    total = 0.0
    i = 0
    while i < n:
        total += 0.1
        i += 1
    return total


def presque_egaux(a, b, eps=1e-9):
    return abs(a - b) <= eps


def table_de_sept():
    i = 1
    while i <= 10:
        print(f"7 x {i} = {7 * i}")
        i += 1


def somme_jusqua(n):
    total = 0
    i = 1
    while i <= n:
        total += i
        i += 1
    return total


def somme_formule(n):
    return n * (n + 1) // 2


def celsius_vers_fahrenheit(c):
    return c * 9 / 5 + 32


def nombre_de_chiffres(n):
    res = 1
    while n >= 10:
        n //= 10
        res += 1
    return res


def calcul_factorielle(n):
    res = 1
    i = 2
    while i <= n:
        res *= i
        i += 1
    return res


def observer_absorption():
    gros = 1e16
    petit = 1.0
    return (gros + petit) == gros


def somme_harmonique_croissante(n):
    total = 0.0
    i = 1
    while i <= n:
        total += 1.0 / i
        i += 1
    return total


def somme_harmonique_decroissante(n):
    total = 0.0
    i = n
    while i >= 1:
        total += 1.0 / i
        i -= 1
    return total


def heron(a, eps=1e-12):
    if a < 0:
        raise ValueError("Valeur négative impossible")
    if a == 0:
        return 0.0
    x = float(a)
    suivant = 0.5 * (x + a / x)
    while abs(suivant - x) > eps * abs(suivant):
        x = suivant
        suivant = 0.5 * (x + a / x)
    return suivant


def vers_binaire(n):
    if n == 0:
        return "0"
    res = ""
    while n > 0:
        res = str(n % 2) + res
        n //= 2
    return res


def epsilon_machine():
    eps = 1.0
    while 1.0 + eps / 2 != 1.0:
        eps /= 2
    return eps


def racines_naif(a, b, c):
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine réelle")
    r = math.sqrt(delta)
    return (-b - r) / (2 * a), (-b + r) / (2 * a)


def racines(a, b, c):
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine réelle")
    r = math.sqrt(delta)
    if b >= 0:
        sure = (-b - r) / (2 * a)
    else:
        sure = (-b + r) / (2 * a)
    autre = c / (a * sure)
    return min(sure, autre), max(sure, autre)


def somme_fractions(n):
    total = Fraction(0)
    i = 0
    while i < n:
        total += Fraction(1, 10)
        i += 1
    return total


q, r = division_euclidienne(2026, 7)
print(q, r, q * 7 + r == 2026)
print(dernier_chiffre(123456789))

print(0.1 + 0.2 == 0.3, presque_egaux(0.1 + 0.2, 0.3), presque_egaux(1.0, 1.5))
s = somme_dixiemes(1000)
print(s, s - 100)

table_de_sept()
print(somme_jusqua(100), somme_formule(100))

print(celsius_vers_fahrenheit(100), celsius_vers_fahrenheit(-40))
print(nombre_de_chiffres(2026), nombre_de_chiffres(7), nombre_de_chiffres(0), nombre_de_chiffres(10 ** 60))
print(calcul_factorielle(5) == 120)
print(observer_absorption() is True)
print(presque_egaux(somme_harmonique_croissante(10000), somme_harmonique_decroissante(10000), eps=1e-10))

print(heron(2), math.sqrt(2), presque_egaux(heron(2), math.sqrt(2), 1e-12))

print(vers_binaire(37), vers_binaire(0), vers_binaire(1024))
ok = True
i = 0
while i < 2000:
    if vers_binaire(i) != bin(i)[2:]:
        ok = False
    i += 1
print(ok)
print(epsilon_machine(), epsilon_machine() == 2 ** -52)

petite, grande = racines_naif(1.0, -1e8, 1.0)
print(petite, grande, petite * grande)
petite, grande = racines(1.0, -1e8, 1.0)
print(petite, grande, petite * grande)
total = somme_fractions(1000)
print(total, total == 100)
print(Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))
