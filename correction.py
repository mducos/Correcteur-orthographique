import sys
from unicodedata import category
import json

# DECLARATION DES VARIABLES GLOBALES 
'''
Les déclarer fait baisser significativement la complexité en temps de
toutes les fonctions.
'''
    # chargement du dictionnaire
tree = open("C:/Users/carol/Desktop/L3/Projet_TAL/structure_arborescente.ttl", "r", encoding="utf-8").readlines()
tree = tree[0]
tree = json.loads(tree)

    # récupération de tous les signes de ponctuation existant grâce à leur unicode car les catégories unicode P* sont destinées à la ponctuation
chrs = (chr(i) for i in range(sys.maxunicode + 1))
punctuation = set(c for c in chrs if category(c).startswith("P"))

    # lecture du fichier 
lines = open("C:/Users/carol/Desktop/L3/Projet_TAL/Lexique383/Lexique383.tsv", "r", encoding="utf-8").readlines()

def typeOfCorrection(corpus):
    '''
    Fonction de départ qui demande à l'utilisateur quel type de 
    correction il souhaite entre une correction automatique et une 
    correction intéractive.
    Cette fonction lance toutes les suivantes pour effectuer la 
    correction souhaitée, et retourne le corpus corrigé.
    '''
    # initialisation de la variable
    type = ""
    # tant que l'utilisateur n'a pas répondu correctement à la question, celle-ci est reposée
    while type == "":
        # question posée pour déterminer si la correction sera automatique ou intéractive
        answer = input("Quel type de correction voulez-vous ? 'automatique' ou 'intéractif' ?\n")
        # si la réponse donnée par l'utilisateur est "automatique"
        if answer == "automatique":
            # on stocke cette réponse
            type = "automatique"
        # si la réponse donnée par l'utilisateur est "intéractif"
        elif answer == "intéractif":
            # on stocke cette réponse
            type = "intéractif"

    return corpusToList(corpus)

def addSpace(str):
    '''
    Fonction qui prend en argument un String et renvoie un String 
    en ayant ajouté des espaces lorsqu’ils n’y étaient pas autour 
    des signes de ponctuation. Ces espaces se trouvent avant les 
    points, les virgules, les parenthèses fermantes et après les 
    parenthèses ouvrantes.

    “Bonjour. Comment allez-vous ?” → 
    “Bonjour . Comment allez-vous ? ”
    '''
    global punctuation

    # on parcourt tous les caractères du string
    for char in str:
        # si le charactère est un signe de ponctuation
        if char in punctuation:
            # les mots contenant un - seront traités plus tard
            if char != "-":
                # on entoure ce caractère d'un espace
                str = str.replace(char, " " + char + " ")
    
    return str

def twoWordsInOne():
    '''
    Fonction qui prend en argument le dictionnaire et renvoie un
    ensemble de strings contenant les mots qui possèdent un espace 
    comme “a capella”.

    fichier (abreuvoir		→ {“a capella”, “a priori”}
            a capella
            a priori
            apporter)
    '''
    global lines

    # création de l'ensemble
    twoWords = set()

    # pour chaque ligne du fichier (la première ligne étant le nom des colonnes, on l'enlève)
    for line in lines[1:]:

        # chaque colonne étant séparée par une tabulation, on les récupère dans une liste
        line = line.split("\t")

        # si un espace est présent dans le mot
        if " " in line[0]:
            # on l'ajoute à l'ensemble
            twoWords.add(line[0])

    return twoWords

def dashInWord():
    '''
    Fonction qui prend en argument le dictionnaire et renvoie un
    ensemble de strings contenant les mots qui possèdent un tiret 
    comme “porte-manteau”.

    fichier (portefeuille   → {porte-manteau”, “porte-clé”}
            porte-manteau
            porte-clé
            portable)
    '''
    global lines

    # création de l'ensemble
    wordWithDash = set()

    # pour chaque ligne du fichier (la première ligne étant le nom des colonnes, on l'enlève)
    for line in lines[1:]:

        # chaque colonne étant séparée par une tabulation, on les récupère dans une liste
        line = line.split("\t")

        # si un tiret est présent dans le mot
        if "-" in line[0]:
            # on l'ajoute à l'ensemble
            wordWithDash.add(line[0])

    return wordWithDash

def corpusToList(corpus):
    '''
    Fonction qui prend en argument un corpus de texte et renvoie une 
    liste de Strings correspondant à sa tokenization. Seuls les espaces
    (“ ”, “\n”, “\t” …) doivent être enlevés. Les mots contenus dans 
    la liste retournée par twoWordsInOne ne doivent pas avoir leur 
    espace supprimé. Les mots contenus dans la liste retournée par 
    dashInWord ne doivent pas avoir leur tiret séparé.

    “Bonjour. Comment allez-vous ?” 
    → [“Bonjour”, “.”, “Comment”, “allez”, “-”, “vous”, “?”]
    '''

    # on commence par ajouter les espaces autour des signes de ponctuation
    corpus = addSpace(corpus)

    # on stocke l'ensemble des mots contenant un espace
    wordWithSpace = twoWordsInOne()
    
    # pour chaque mot de cet ensemble, on vérifie s'il est dans le corpus
    for word in wordWithSpace:
        if word in corpus.lower():
            # s'il y est, on change l'espace en un signe présent dans aucun mot pour pouvoir le reconnaître plus tard
            corpus = corpus.replace(word, word.replace(" ", "*"))
            # mais si le mot a une majuscule au début, il faut le traiter ainsi
            word = word[0].upper() + word[1:]
            corpus = corpus.replace(word, word.replace(" ", "*"))

    # en splitant, les composants d'un mot qui contient originellement un espace ne sont plus séparés
    corpus = corpus.split()

    # pour chaque mot du corpus
    for i in range(len(corpus)):
        # s'il contient * signifie que c'est un mot à plusieurs composants
        if "*" in corpus[i]:
            # on remet l'espace
            corpus[i] = corpus[i].replace("*", " ")

    # on stocke l'ensemble des mots contenant un tiret
    wordWithDash = dashInWord()
    
    # pour chaque mot du corpus
    for i in range(len(corpus)):
        # s'il contient un tiret
        if "-" in corpus[i]:
            # on vérifie qu'il ne fait pas partie de l'ensemble des mots à tiret
            if not(corpus[i].lower() in wordWithDash):
                # on ajoute les espaces nécessaires autour de la ponctuation
                corpus[i] = corpus[i].replace("-", " - ")
                # on transforme l'expression en liste
                listWord = corpus[i].split()
                # on supprime le faux mot avec tiret dans le corpus
                del corpus[i]
                # et on ajoute à l'indice i tous les mots de la liste
                for component in reversed(listWord):
                    corpus.insert(i, component)

    return corpus

def rechercheWordDict(word):
    '''
    Fonction qui prend un String en argument et renvoie un booléen, 
    vrai si le String est présent dans le dictionnaire, faux s’il 
    n’y est pas. Pour cela, il faut que le mot comparé soit totalement 
    en minuscule (mais il ne faut pas que le mot lui-même ait été 
    modifié). Si le string est un signe de ponctuation, il n’est pas 
    comparé.

    "Xylophone" → True
    "xylophone" → True
    "xylopone" → False
    '''
    global tree
    global punctuation

    # si le mot n'est pas un signe de ponctuation
    if not(word in punctuation):
        # on parcourt chaque lettre du mot pour vérifier qu'elles sont des noeuds/feuilles dans l'arbre
        return recherche_letter(tree, word.lower())


def recherche_letter(tree, word):
    '''
    Fonction qui prend un arbre lexicologique et un String en argument 
    et renvoie un booléen, vrai si le String est présent dans l'arbre,
    faux s'il n'y est pas.
    "xylophone" → True
    "xylopone" → False
    '''

    # cas de base : on lit la dernière lettre du mot
    if len(word) == 1:
        # la suite de lettres est dans l'arbre et la dernière lettre est finale donc c'est un mot du dictionnaire
        if "*" in tree[word]:
            return True
        # la suite de lettres est dans l'arbre mais la dernière lettre n'est pas finale donc ce n'est pas un mot du dictionnaire
        else:
            return False
    # si la première lettre est dans les clés du dictionnaire, on poursuit la recherche
    elif word[0] in tree:
        return recherche_letter(tree[word[0]], word[1:])
    # si elle n'y est pas, on peut dès à présent retourner faux
    else:
        return False

import numpy as np




corpus = "Pour ceux qui ont la décence de ne pas avoir Facebook, je vous résume. Loudblast (groupe de death français) qui fait une publi pour mettre en avant un t-shirt de Hatecouture (une page de t-shirt cynique bête et méchant) avec la gueule d'Emile Louis.Jean Peu Plus de cette culture de la provoc' à trois balle de la sc metal... a cappella."
list = typeOfCorrection(corpus)
for word in list:
    print(word, rechercheWordDict(word), end=", ")
