import sys
from unicodedata import category
import json





# DECLARATION DES VARIABLES GLOBALES 





'''
Les déclarer fait baisser significativement la complexité en temps de
toutes les fonctions.
'''
    # chargement des fichiers
tree = json.loads(open("C:/Users/carol/Desktop/L3/Projet_TAL/structure_arborescente.ttl", "r", encoding="utf-8").readlines()[0])
wordsWithSpace = json.loads(open("C:/Users/carol/Desktop/L3/Projet_TAL/two_words_in_one.ttl", "r", encoding="utf-8").readlines()[0])
wordsWithDash = json.loads(open("C:/Users/carol/Desktop/L3/Projet_TAL/words_with_dash.ttl", "r", encoding="utf-8").readlines()[0])

    # récupération de tous les signes de ponctuation existant grâce à leur unicode car les catégories unicode P* sont destinées à la ponctuation
chrs = (chr(i) for i in range(sys.maxunicode + 1))
punctuation = set(c for c in chrs if category(c).startswith("P"))





# ALGORITHME DE RECONNAISSANCE DES MOTS FAUTIFS OU NON





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

    global wordsWithDash
    global wordsWithSpace

    # on commence par ajouter les espaces autour des signes de ponctuation
    corpus = addSpace(corpus)
    
    # pour chaque mot de cet ensemble, on vérifie s'il est dans le corpus
    for word in wordsWithSpace:
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
    
    # pour chaque mot du corpus
    for i in range(len(corpus)):
        # s'il contient un tiret
        if "-" in corpus[i]:
            # on vérifie qu'il ne fait pas partie de l'ensemble des mots à tiret
            if not(corpus[i].lower() in wordsWithDash):
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
        return rechercheWordRec(tree, word.lower())


def rechercheWordRec(tree, word):
    '''
    Fonction qui, à partir du fichier contenant l'arbre du vocabulaire
    et d'un mot, cherche dans l'arbre si le mot y est présent.
    La fonction retourne un booléen.
    "xylophone" → True
    "xylopone" → False
    '''
    
    # cas de base : on lit la dernière lettre du mot
    if len(word) == 1:
        # la suite de lettres est dans l'arbre mais la dernière lettre n'y est pas donc ce n'est pas un mot du dictionnaire
        if not(word in tree):
            return False
        # la suite de lettres est dans l'arbre alors pour toutes les clés dans l'arbre
        for key in tree[word]:
            # vérifier s'il est possible de convertir en float ce qui signifierait que la lettre est finale et donc le mot existe
            try:
                float(key)
                return float(key)
            except:
                pass
        # la suite de lettres est dans l'arbre mais la dernière lettre n'est pas finale donc ce n'est pas un mot du dictionnaire
        return False
    # si la première lettre est dans les clés du dictionnaire, on poursuit la recherche
    elif word[0] in tree:
        return rechercheWordRec(tree[word[0]], word[1:])
    # si elle n'y est pas, on peut dès à présent retourner faux
    else:
        return False





# ALGORITHME CREE PAR PETER NORVIG





def edits1(word):
    '''
    Fonction qui, à partir d'un mot, retourne l'ensemble de tous les mots
    d'une distance de 1 avec celui-ci grâce à des opérations de suppression,
    transposition, substitution et insertion.
    '''

    # ensemble des lettres de la langue française
    letters    = 'abcdefghijklmnopqrstuvwxyzàâæçéèêëîïôœùûüÿ-'
    # découpage du mot pour y insérer les opérations
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    # suppression
    deletes    = [L + R[1:]               for L, R in splits if R]
    # transposition
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    # substitution
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    # insertion
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    '''
    Fonction qui, à partir d'un mot, retourne l'ensemble de tous les mots
    d'une distance de 1 avec celui-ci grâce à des opérations de suppression,
    transposition, substitution et insertion.
    '''

    # retourne l'ensemble de tous les mots générés avec une distance de 1 avec les mots générés avec une distance de 1
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits3(word): 
    '''
    Fonction qui, à partir d'un mot, retourne l'ensemble de tous les mots
    d'une distance de 2 avec celui-ci grâce à des opérations de suppression,
    transposition, substitution et insertion.
    '''

    # retourne l'ensemble de tous les mots générés avec une distance de 1 avec les mots générés avec une distance de 1 avec les mots générés avec une distance de 1
    return set(e3 for e1 in edits1(word) for e2 in edits1(e1) for e3 in edits1(e2))

def known(words): 
    '''
    Fonction qui, à partir d'un ensemble de mots, retourne un ensemble de
    ceux qui sont présents dans le dictionnaire.
    '''

    global tree
    # retourne l'ensemble des mots qui existe dans l'arbre lexicographique
    return set(w for w in words if rechercheWordRec(tree, w))

def probabilite(word):
    '''
    Fonction qui, à partir d'un mot, retourne la probabilité qu'il 
    apparraisse dans un corpus.
    '''

    global tree
    return frequence_relative(tree, word)

def frequence_relative(tree, word):
    '''
    Fonction qui, à partir d'un mot et du dictionnaire, renvoie sa fréquence
    relative. Celle-ci est donnée dans l'arbre lexicographique à la fin
    de la lecture du mot.
    '''
    
    # cas de base : on lit la dernière lettre du mot
    if len(word) == 1:
        # la suite de lettres est dans l'arbre alors pour toutes les clés dans l'arbre
        for key in tree[word]:
            # vérifier s'il est possible de convertir en float ce qui signifierait que la lettre est finale et donc le mot existe
            try:
                float(key)
                return float(key)
            except:
                pass
        return 0.0
    # si la première lettre est dans les clés du dictionnaire, on poursuit la recherche
    return frequence_relative(tree[word[0]], word[1:])

def correction(word): 
    '''
    Fonction qui, à partir d'un mot, détermine quelle est la meilleure
    correction possible s'il n'est pas dans le dictionnaire
    '''

    global tree

    # ensemble des mots dans le dictionnaire à partir des mots distants de 0 du mot de base
    word_distance0 = known([word])
    # si au moins un mot parmi cet ensemble est dans le dictionnaire
    if len(word_distance0) > 0:
        # retourne le mot qui a la probabilité maximum
        return max(word_distance0, key=probabilite)

    # ensemble des mots dans le dictionnaire à partir des mots distants de 1 du mot de base
    word_distance1 = known(edits1(word))
    # si au moins un mot parmi cet ensemble est dans le dictionnaire
    if len(word_distance1) > 0:
        # retourne le mot qui a la probabilité maximum
        return max(word_distance1, key=probabilite)

    # ensemble des mots dans le dictionnaire à partir des mots distants de 2 du mot de base
    word_distance2 = known(edits2(word))
    # si au moins un mot parmi cet ensemble est dans le dictionnaire
    if len(word_distance2) > 0:
        # retourne le mot qui a la probabilité maximum
        return max(word_distance2, key=probabilite)

    # si aucun mot d'une distance de 2 ou moins n'a été trouvé, 
    return (word, "not found")





# ALGORITHME POUR CORRECTION AUTOMATIQUE OU INTERACTIVE





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





# LANCEMENT DU PROGRAMME DE CORRECTION





'''Hallo ceux qui ont la décence de ne pas avoir Facebook, je vous résume. 
Loudblast (groupe de death français) qui fait une publi pour mettre en 
avant un t-shirt de Hatecouture (une page de t-shirt cynique bête et 
méchant) avec la gueule d'Emile Louis.Jean Peu Plus de cette culture 
de la provoc' à trois balle de la sc metal... a cappella.'''

corpus = "Hallo Pour ceux qui ont la décence de ne pas avoir Facebook, je vous résume. Loudblast (groupe de death français) qui fait une publi pour mettre en avant un t-shirt de Hatecouture (une page de t-shirt cynique bête et méchant) avec la gueule d'Emile Louis.Jean Peu Plus de cette culture de la provoc' à trois balle de la sc metal... a cappella. haute-couture"
list = typeOfCorrection(corpus)
for word in list:
    if rechercheWordDict(word) == False:
        print(word, "→", correction(word))
    else:
        print(word)


# TODO : voir si on ne peut pas intégrer la fonction de freq rel à celle de recherche rec pour gagner du temps d'exécution (pas sûre que ce soit possible)