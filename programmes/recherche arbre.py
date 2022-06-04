import json

# chargement du fichier
tree = json.loads(open("C:/Users/carol/Desktop/L3/Projet_TAL/structure_arborescente.ttl", "r", encoding="utf-8").readlines()[0])

def recherche_word(tree, word):
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
        return recherche_word(tree[word[0]], word[1:])
    # si elle n'y est pas, on peut dès à présent retourner faux
    else:
        return False

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

    # sérialization à l'aide de json (ie enregistrement dans un fichier pour pouvoir l'utiliser plus tard dans d'autres programmes)
    with open("C:/Users/carol/Desktop/L3/Projet_TAL/two_words_in_one.ttl", "w", encoding='utf-8' ) as df: # chemin d'accès pour Mathilde
    #with open("", "w", encoding='utf-8' ) as df: # chemin d'accès pour Xin
        json.dump(list(twoWords), df, ensure_ascii=False)
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

    # sérialization à l'aide de json (ie enregistrement dans un fichier pour pouvoir l'utiliser plus tard dans d'autres programmes)
    with open("C:/Users/carol/Desktop/L3/Projet_TAL/words_with_dash.ttl", "w", encoding='utf-8' ) as df: # chemin d'accès pour Mathilde
    #with open("", "w", encoding='utf-8' ) as df: # chemin d'accès pour Xin
        json.dump(list(wordWithDash), df, ensure_ascii=False)
    return wordWithDash
