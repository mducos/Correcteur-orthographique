import requests
import sys
from unicodedata import category

# enregistrement de l'arbre lexicographique
tree = requests.get("https://github.com/mducos/Correction-automatique/raw/main/production/structure_arborescente.json").json()

# récupération de tous les signes de ponctuation existant grâce à leur unicode car les catégories unicode P* sont destinées à la ponctuation
chrs = (chr(i) for i in range(sys.maxunicode + 1))
punctuation = set(c for c in chrs if category(c).startswith("P"))

def addSpace(str):
    '''
    Fonction qui prend en argument un String et renvoie un String en ayant ajouté des espaces 
    lorsqu’ils n’y étaient pas autour des signes de ponctuation. Ces espaces se trouvent avant les 
    points, les virgules, les parenthèses fermantes et après les parenthèses ouvrantes.
    
    “Bonjour. Comment allez-vous ?” → “Bonjour . Comment allez-vous ? ”
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
    Fonction qui prend en argument un corpus de texte et renvoie une liste de Strings 
    correspondant à sa tokenization. Seuls les espaces (“ ”, “\n”, “\t” …) doivent être enlevés. 
    Les mots contenus dans la liste retournée par twoWordsInOne ne doivent pas avoir leur espace 
    supprimé. Les mots contenus dans la liste retournée par dashInWord ne doivent pas avoir 
    leur tiret séparé.
    
    “Bonjour. Comment allez-vous ?” → [“Bonjour”, “.”, “Comment”, “allez”, “-”, “vous”, “?”]
    '''

    global wordsWithDash
    global woredsWithSpace
    global wordsWithApostrophe

    # pour chaque mot de l'ensemble des mots avec une apostrophe de plus de 2 caractères (pour enlever les "l'" et "d'"), on vérifie s'il est dans le corpus
    for word in wordsWithApostrophe:
        if word in corpus.lower() and len(word) > 2:
            # s'il y est, on change l'apostrophe en un signe présent dans aucun mot pour pouvoir le reconnaître plus tard
            corpus = corpus.replace(word, word.replace("'", "$"))
            # mais si le mot a une majuscule au début, il faut le traiter ainsi
            word = word[0].upper() + word[1:]
            corpus = corpus.replace(word, word.replace("'", "$"))

    # ajout des espaces autour des signes de ponctuation
    corpus = addSpace(corpus)

    # pour chaque mot de l'ensemble des mots à 2 composés, on vérifie s'il est dans le corpus
    for word in wordsWithSpace:
        # on doit faire comme si les apostrophes étaient sous forme d'apostrophe
        if word in corpus.replace("$", "'").lower():
            # s'il y est, on change l'espace en un signe présent dans aucun mot pour pouvoir le reconnaître plus tard
            corpus = corpus.replace(word.replace("'", "$"), word.replace("'", "$").replace(" ", "*"))
            # mais si le mot a une majuscule au début, il faut le traiter ainsi
            word = word[0].upper() + word[1:]
            corpus = corpus.replace(word.replace("'", "$"), word.replace("'", "$").replace(" ", "*"))

    # en splitant, les composants d'un mot qui contient originellement un espace ne sont plus séparés
    corpus = corpus.split()
    # pour chaque mot du corpus
    for i in range(len(corpus)):
        # s'il contient * signifie que c'est un mot à plusieurs composants
        if "$" in corpus[i]:
            # on remet l'espace
            corpus[i] = corpus[i].replace("$", "'")
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
    Fonction qui prend un String en argument et renvoie un booléen, vrai si le String est 
    présent dans le dictionnaire, faux s’il n’y est pas. Pour cela, il faut que le mot comparé 
    soit totalement en minuscule (mais il ne faut pas que le mot lui-même ait été modifié). 
    Si le string est un signe de ponctuation, il n’est pas comparé.

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
    Fonction qui, à partir du fichier contenant l'arbre du vocabulaire et d'un mot, cherche dans 
    l'arbre si le mot y est présent. S'il l'est, cette fonction renvoie la fréquence du mot. La 
    fonction retourne un booléen.

    "xylophone" → 2.2e-8
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
                return float(key)
            except:
                pass
        # la suite de lettres est dans l'arbre mais la dernière lettre n'est pas finale donc ce n'est pas un mot du dictionnaire
        return False
    # si les opérations ont généré le mot vide
    elif len(word) == 0:
        return False
    # si la première lettre est dans les clés du dictionnaire, on poursuit la recherche
    elif word[0] in tree:
        return rechercheWordRec(tree[word[0]], word[1:])
    # si elle n'y est pas, on peut dès à présent retourner faux
    else:
        return False
        
