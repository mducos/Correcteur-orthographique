from audioop import add
import sys
from unicodedata import category

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

    # récupération de tous les signes de ponctuation existant grâce à leur unicode car les catégories unicode P* sont destinées à la ponctuation
    chrs = (chr(i) for i in range(sys.maxunicode + 1))
    punctuation = set(c for c in chrs if category(c).startswith("P"))

    # on parcourt tous les caractères du string
    for char in str:
        # si le charactère est un signe de ponctuation
        if char in punctuation:
            # les mots contenant un - seront traités plus tard
            if char != "-":
                # on entoure ce caractère d'un espace
                str = str.replace(char, " " + char + " ")
    
    return str

def twoWordsInOne(file):
    '''
    Fonction qui prend en argument le dictionnaire et renvoie un
    ensemble de strings contenant les mots qui possèdent un espace 
    comme “a capella”.

    fichier (abreuvoir		→ {“a capella”, “a priori”}
            a capella
            a priori
            apporter)
    '''
    
    # création de l'ensemble
    twoWords = set()

    # lecture du fichier 
    lines = open(file, "r", encoding="utf-8").readlines()

    # pour chaque ligne du fichier (la première ligne étant le nom des colonnes, on l'enlève)
    for line in lines[1:]:

        # chaque colonne étant séparée par une tabulation, on les récupère dans une liste
        line = line.split("\t")

        # si un espace est présent dans le mot
        if " " in line[0]:
            # on l'ajoute à l'ensemble
            twoWords.add(line[0])

    return twoWords

def dashInWord(file):
    '''
    Fonction qui prend en argument le dictionnaire et renvoie un
    ensemble de strings contenant les mots qui possèdent un tiret 
    comme “porte-manteau”.

    fichier (portefeuille   → {porte-manteau”, “porte-clé”}
            porte-manteau
            porte-clé
            portable)
    '''
    
    # création de l'ensemble
    wordWithDash = set()

    # lecture du fichier 
    lines = open(file, "r", encoding="utf-8").readlines()

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
    wordWithSpace = twoWordsInOne("C:/Users/carol/Desktop/L3/Projet_TAL/Lexique383/Lexique383.tsv")
    
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
    wordWithDash = dashInWord("C:/Users/carol/Desktop/L3/Projet_TAL/Lexique383/Lexique383.tsv")
    
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

