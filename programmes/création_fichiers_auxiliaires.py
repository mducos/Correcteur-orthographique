import requests

# lecture du dictionnaire sous format tsv 
lines = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/Lexique383.tsv").text.split("\n")

def twoWordsInOne():
    '''
    Fonction qui prend en argument le dictionnaire et renvoie un ensemble de strings 
    contenant les mots qui possèdent un espace.
    fichier (abreuvoir, a capella, a priori, apporter) → {“a capella”, “a priori”}
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
    Fonction qui prend en argument le dictionnaire et renvoie un ensemble de strings 
    contenant les mots qui possèdent un tiret.
    fichier (portefeuille, porte-manteau, porte-clé, portable) → {"porte-manteau", "porte-clé"}
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

def apostropheInWord():
    '''
    Fonction qui prend en argument le dictionnaire et renvoie un ensemble de strings 
    contenant les mots qui possèdent une apostrophe.
    fichier(ajourné, aujourd'hui, au) → {"aujourd'hui"}
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

    return wordWithApostrophe
