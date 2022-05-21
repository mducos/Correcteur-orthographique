import json

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
    {"a": {"r": {"b": {"r": {"e": {}
                             "i": {"s": {"s": {"a": {"u": {"t": {}}}}}}}}}
           "v": {"o": {"i": {"r": {}}}}}, 
     "b": {...}
    }
    '''

    # lecture du fichier 
    lines = open(file, "r", encoding="utf-8").readlines()
    # création de la structure arborescente
    voca2tree = dict()

    # pour chaque ligne du fichier (la première ligne étant le nom des colonnes, on l'enlève)
    for line in lines[1:]:

        # chaque colonne étant séparée par une tabulation, on les récupère dans une liste
        line = line.split("\t")
        #print("line :", line)# TODO
        # simplification des variables
        word = line[0]
        #print("word :", word)# TODO
        # création des clés correspondant à la première lettre de chaque mot
        
        letter2letter_maker(word, voca2tree)
    
    # sérialization à l'aide de json 
    with open("C:/Users/carol/Desktop/L3/Projet_TAL/structure_arborescente.ttl", "w", encoding='utf-8' ) as df:
        json.dump(voca2tree, df, ensure_ascii=False)
    #print(voca2tree)        



def letter2letter_maker(word, letter2letter):
    '''
    Fonction définie par récursion qui, à partir d'un mot, construit 
    la suite de dictionnaire qui y correspond.
    "avoir" → {'a': {'v': {'o': {'i': {'r': {}}}}}}
    '''
    # cas de base, si le mot est fini on retourne un dictionnaire vide
    if len(word) == 1:
        if not(word[0] in letter2letter):
            #print(word[0], "not in dico", letter2letter)
            tmp = dict()
            tmp["*"] = dict()
            #letter2letter[word[0]] = tmp
            #print(type(word[0]))
            letter2letter[word[0]] = dict()
            
        else:
            tmp = dict()
            tmp[word] = "*"
            #letter2letter = {**letter2letter[word[0]], **tmp}
            letter2letter = {**letter2letter[word[0]], **dict()}
        return letter2letter
    # si le mot n'est pas fini, on construit le dictionnaire qui correspond au reste du mot
    else:
        if not(word[0] in letter2letter):
            #print(word[0], "not in dico")
            letter2letter[word[0]] = dict()
            #print("dico :", letter2letter)
        #letter2letter[word[0]] = {**letter2letter, }
        letter2letter[word[0]] = {**letter2letter[word[0]], **letter2letter_maker(word[1:], letter2letter[word[0]])}
        #print("dico", letter2letter, "\n")
        return letter2letter



vocab2tree("C:/Users/carol/Desktop/L3/Projet_TAL/Lexique383/Lexique383.tsv") # chemin d'accès pour Mathilde
#vocab2tree("") # chemin d'accès pour Xin
