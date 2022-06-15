import json
# lecture du dictionnaire sous format tsv 
lines = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/Lexique383.tsv").text.split("\n")

def vocab2tree(file):
    '''
    Fonction qui, à partir d'un fichier contenant le lexique, renvoie 
    la structure arborescente correspondante.
    Cette structure se présente sous la forme d'un dictionnaire de string
    vers des dictionnaires, contenant autant de clés que de premier 
    caractère possible dans les mots du vocabulaire.
    Les dictionnaires en valeur se construisent sur la même forme du 
    premier dictionnaire, c'est-à-dire sont des dictionnaires de string
    vers des dictionnaires.
    Lorsqu'un mot se termine, la valeur est un dictionnaire vide.
    Schéma :
    {"a": {"r": {"b": {"r": {"e": {1.1e-08: {}}
                             "i": {"s": {"s": {"a": {"u": {"t": {1.8e-09: {}}}}}}}}}}
           "v": {"o": {"i": {"r": {3.4e-07: {}}}}}}, 
     "b": {...}
    }
    '''

    global lines

    # création de la structure arborescente
    voca2tree = dict()

    # pour chaque ligne du fichier (la première ligne étant le nom des colonnes, on l'enlève) jusqu'au dernier mot
    for line in lines[1:142695]:
        # chaque colonne étant séparée par une tabulation, on les récupère dans une liste
        line = line.split("\t")

        # simplification des variables, on ajoute un * au mot pour signifier une fin de mot (caractère unique comme <f>)
        word = line[0] + "*"
        freq_rel = (float(line[8]) + float(line[9])) / (2*10e6)

        # création des clés correspondant à la première lettre de chaque mot, par récurrence
        letter2letter_maker(word, voca2tree, freq_rel)

    return voca2tree

def letter2letter_maker(word, letter2letter, freq_rel):
    '''
    Fonction définie par récursion qui, à partir d'un mot, construit 
    la suite de dictionnaire qui y correspond.
    "avoir" → {'a': {'v': {'o': {'i': {'r': {'0.002': {}}}}}}}
    '''
    
    # cas de base, si le mot est fini on retourne un dictionnaire vide
    if len(word) == 1:
        # pour toutes les clés déjà présentes
        for key in letter2letter:
            # si une clé est un float, c'est-à-dire si le mot est déjà présent dans l'arbre (ce qui arrive pour les mots avec plusieurs catégories syntaxiques)
            if isinstance(key, float):
                # somme des fréquences relatives
                freq_rel = freq_rel + key
                # suppression de l'ancienne fréquence relative
                del letter2letter[key]
                # création de la nouvelle clé avec la fréquence relative
                letter2letter[freq_rel + key] = dict()
                return letter2letter
        # si aucune clé n'est un float, ie si le mot n'est pas déjà présent dans l'arbre, création de la feuille avec la fréquence relative du mot en clé
        letter2letter[freq_rel] = dict()
        return letter2letter
        
    # si le mot n'est pas fini, on construit le dictionnaire qui correspond au reste du mot
    else:
        # si le noeud de la lettre n'existe pas, on la crée
        if not(word[0] in letter2letter):
            letter2letter[word[0]] = dict()
        # on entre dans le sous-arbre relié par le noeud et on continue la lecture du mot
        letter2letter[word[0]] = {**letter2letter[word[0]], **letter2letter_maker(word[1:], letter2letter[word[0]], freq_rel)}
        return letter2letter
    
        if not(word[0] in letter2letter):
            letter2letter[word[0]] = dict()
        # on entre dans le sous-arbre relié par le noeud et on continue la lecture du mot
        letter2letter[word[0]] = {**letter2letter[word[0]], **letter2letter_maker(word[1:], letter2letter[word[0]], freq_rel)}
        return letter2letter
