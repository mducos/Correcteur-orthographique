import json

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
    with open("C:/Users/carol/Desktop/L3/Projet_TAL/two_words_in_one.json", "w", encoding='utf-8' ) as df: # chemin d'accès pour Mathilde
    #with open("", "w", encoding='utf-8' ) as df: # chemin d'accès pour Xin
        json.dump(list(twoWords), df, ensure_ascii=False)
    return twoWords

def dashInWord():
    '''
    Fonction qui prend en argument le dictionnaire et renvoie un
    ensemble de strings contenant les mots qui possèdent un tiret 
    comme “porte-manteau”.

    fichier (portefeuille   → {"porte-manteau", "porte-clé"}
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
    with open("C:/Users/carol/Desktop/L3/Projet_TAL/words_with_dash.json", "w", encoding='utf-8' ) as df: # chemin d'accès pour Mathilde
    #with open("", "w", encoding='utf-8' ) as df: # chemin d'accès pour Xin
        json.dump(list(wordWithDash), df, ensure_ascii=False)
    return wordWithDash


def apostropheInWord():
    '''
    Fonction qui prend en argument le dictionnaire et renvoie un
    ensemble de strings contenant les mots qui possèdent une 
    apostrophe comme "aujourd'hui".

    fichier (ajourné       → {"aujourd'hui"}
            aujourd'hui
            au)
    '''
    global lines

    # création de l'ensemble
    wordWithApostrophe = set()

    # pour chaque ligne du fichier (la première ligne étant le nom des colonnes, on l'enlève)
    for line in lines[1:]:

        # chaque colonne étant séparée par une tabulation, on les récupère dans une liste
        line = line.split("\t")

        # si un tiret est présent dans le mot
        if "'" in line[0]:
            # on l'ajoute à l'ensemble
            wordWithApostrophe.add(line[0])

    # sérialization à l'aide de json (ie enregistrement dans un fichier pour pouvoir l'utiliser plus tard dans d'autres programmes)
    with open("C:/Users/carol/Desktop/L3/Projet_TAL/words_with_apostrophe.json", "w", encoding='utf-8' ) as df: # chemin d'accès pour Mathilde
    #with open("", "w", encoding='utf-8' ) as df: # chemin d'accès pour Xin
        json.dump(list(wordWithApostrophe), df, ensure_ascii=False)
    return wordWithApostrophe

