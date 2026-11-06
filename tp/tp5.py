import random
import unicodedata


def lettre_vers_nombre(c):
    return ord(c) - ord("A")


def nombre_vers_lettre(n):
    return chr(n % 26 + ord("A"))


def nettoyer(texte):
    maj = unicodedata.normalize("NFD", texte).upper()
    res = ""
    i = 0
    while i < len(maj):
        if "A" <= maj[i] <= "Z":
            res += maj[i]
        i += 1
    return res


def chiffrer(texte, a, b):
    propre = nettoyer(texte)
    res = ""
    i = 0
    while i < len(propre):
        x = lettre_vers_nombre(propre[i])
        res += nombre_vers_lettre((a * x + b) % 26)
        i += 1
    return res


def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def cles_valides():
    res = []
    a = 1
    while a <= 25:
        if pgcd(a, 26) == 1:
            res.append(a)
        a += 1
    return res


valides = cles_valides()


def inverse_modulaire(a, n):
    a = a % n
    k = 1
    while k < n:
        if (a * k) % n == 1:
            return k
        k += 1
    raise ValueError(f"{a} n'est pas inversible modulo {n}")


def dechiffrer(texte, a, b):
    a_inv = inverse_modulaire(a, 26)
    propre = nettoyer(texte)
    res = ""
    i = 0
    while i < len(propre):
        y = lettre_vers_nombre(propre[i])
        res += nombre_vers_lettre(a_inv * (y - b) % 26)
        i += 1
    return res


def toutes_les_clefs(secret):
    res = []
    i = 0
    while i < len(valides):
        b = 0
        while b < 26:
            res.append((valides[i], b, dechiffrer(secret, valides[i], b)))
            b += 1
        i += 1
    return res


def compter_lettres(texte):
    comptes = {}
    i = 0
    while i < len(texte):
        comptes[texte[i]] = comptes.get(texte[i], 0) + 1
        i += 1
    return comptes


def lettre_la_plus_frequente(texte):
    comptes = compter_lettres(texte)
    lettres = list(comptes.keys())
    meilleure = lettres[0]
    i = 1
    while i < len(lettres):
        if comptes[lettres[i]] > comptes[meilleure]:
            meilleure = lettres[i]
        i += 1
    return meilleure


def casser_par_frequences(secret):
    cible = lettre_vers_nombre(lettre_la_plus_frequente(secret))
    res = []
    i = 0
    while i < len(valides):
        a = valides[i]
        b = (cible - 4 * a) % 26
        res.append((a, b, dechiffrer(secret, a, b)))
        i += 1
    return res


def indice_coincidence(texte):
    n = len(texte)
    comptes = list(compter_lettres(texte).values())
    total = 0
    i = 0
    while i < len(comptes):
        total += comptes[i] * (comptes[i] - 1)
        i += 1
    return total / (n * (n - 1))


def vigenere(texte, cle):
    propre = nettoyer(texte)
    res = ""
    i = 0
    while i < len(propre):
        decalage = lettre_vers_nombre(cle[i % len(cle)])
        res += nombre_vers_lettre(lettre_vers_nombre(propre[i]) + decalage)
        i += 1
    return res


def indices_par_longueur(secret, l_max):
    res = []
    L = 1
    while L <= l_max:
        total = 0
        i = 0
        while i < L:
            total += indice_coincidence(secret[i::L])
            i += 1
        res.append((L, total / L))
        L += 1
    return res


texte_long = nettoyer(
    "Le chiffrement affine est un chiffrement par substitution monoalphabetique. "
    "Chaque lettre du message est remplacee par une autre lettre, toujours la meme, "
    "ce qui laisse intactes les frequences relatives des lettres et permet de casser "
    "le code sans essayer toutes les clefs possibles."
)

print(lettre_vers_nombre("C"), nombre_vers_lettre(2), nettoyer("Été, à Paris !"))
print(chiffrer("ATTAQUEALAUBE", 5, 8), chiffrer("ATTAQUEALAUBE", 1, 3))
print(valides, len(valides), inverse_modulaire(5, 26))
try:
    inverse_modulaire(4, 26)
except ValueError as erreur:
    print("erreur attendue :", erreur)

message = nettoyer("Attaque a l aube")
secret = chiffrer(message, 5, 8)
print(secret, dechiffrer(secret, 5, 8), dechiffrer(secret, 5, 8) == message)
try:
    dechiffrer(secret, 4, 7)
except ValueError as erreur:
    print("clé refusée :", erreur)

essais = toutes_les_clefs(secret)
print(len(essais), "clés essayées")
i = 0
while i < len(essais):
    if essais[i][2] == message:
        print("la bonne clé :", essais[i][0], essais[i][1])
    i += 1

secret_long = chiffrer(texte_long, 7, 12)
candidats = casser_par_frequences(secret_long)
print(len(candidats), "candidats au lieu de 312")
i = 0
while i < len(candidats):
    if candidats[i][2].startswith("LECHIFFREMENT"):
        print("trouvé :", candidats[i][0], candidats[i][1], candidats[i][2][:40])
    i += 1
court = casser_par_frequences(chiffrer("ATTAQUEALAUBE", 5, 8))
trouve = False
i = 0
while i < len(court):
    if court[i][2] == "ATTAQUEALAUBE":
        trouve = True
    i += 1
print("message court retrouvé par fréquences :", trouve)

random.seed(1)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
hasard = ""
i = 0
while i < len(texte_long):
    hasard += random.choice(alphabet)
    i += 1
print(indice_coincidence(texte_long), indice_coincidence(secret_long), indice_coincidence(hasard))
secret_vigenere = vigenere(texte_long, "CLE")
print(secret_vigenere[:40], indice_coincidence(secret_vigenere))
print(indices_par_longueur(secret_vigenere, 7))
