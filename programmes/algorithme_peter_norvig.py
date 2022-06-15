import requests

# enregistrement de l'arbre lexicographique
tree = requests.get("https://github.com/mducos/Correction-automatique/raw/main/production/structure_arborescente.json").json()

def edits1(word):
    '''
    Fonction qui, à partir d'un mot, retourne l'ensemble de tous les mots d'une distance de 1 
    avec celui-ci grâce à des opérations de suppression, transposition, substitution et 
    insertion.
    '''

    # ensemble des lettres de la langue française (plus le trait d'union dans les cas comme portemanteau à corriger en porte-manteau)
    letters    = 'abcdefghijklmnopqrstuvwxyzàâæçéèêëîïôœùûüÿ-'
    # découpage du mot pour y insérer les opérations
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]

    deletes    = [L + R[1:]               for L, R in splits if R] # suppression
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1] # transposition
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters] # substitution
    inserts    = [L + c + R               for L, R in splits for c in letters] # insertion
    
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    '''
    Fonction qui, à partir d'un mot, retourne l'ensemble de tous les mots d'une distance de 1 
    avec celui-ci grâce à des opérations de suppression, transposition, substitution et insertion.
    '''

    # retourne l'ensemble de tous les mots générés avec une distance de 1 avec les mots générés avec une distance de 1
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

def known(words): 
    '''
    Fonction qui, à partir d'un ensemble de mots, retourne un ensemble de ceux qui sont présents 
    dans le dictionnaire.
    '''

    global tree
    # retourne l'ensemble des mots qui existe dans l'arbre lexicographique
    return set(w for w in words if rechercheWordRec(tree, w))

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
                return True
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

def probabilite(word):
    '''
    Fonction qui, à partir d'un mot, retourne la probabilité qu'il apparraisse dans un corpus.
    '''

    global tree
    
    return frequence_relative(tree, word)

def frequence_relative(tree, word):
    '''
    Fonction qui, à partir d'un mot et du dictionnaire, calcule sa fréquence
    relative. Celle-ci est donnée dans l'arbre lexicographique à la fin
    de la lecture du mot.
    '''
    
    # cas de base : on lit la dernière lettre du mot
    if len(word) == 1:
        # la suite de lettres est dans l'arbre alors pour toutes les clés dans l'arbre
        for key in tree[word]:
            # vérifier s'il est possible de convertir en float ce qui signifierait que la lettre est finale et donc le mot existe
            try:
                return float(key)
            except:
                pass

        return 0.0
    # si la première lettre est dans les clés du dictionnaire, on poursuit la recherche
    return frequence_relative(tree[word[0]], word[1:])

def correctionAuto(word): 
    '''
    Fonction qui, à partir d'un mot, détermine quelle est la meilleure correction possible s'il 
    n'est pas dans le dictionnaire.
    '''

    global tree

    # ensemble des mots dans le dictionnaire à partir des mots distants de 0 du mot de base (ie le mot pris en argument)
    word_distance0 = known([word])
    # si au moins un mot parmi cet ensemble est dans le dictionnaire (ie si le mot est connu)
    if len(word_distance0) > 0:
        # retourne le mot qui a la probabilité maximum (ie le mot pris en argument)
        return max(word_distance0, key=probabilite)

    # ensemble des mots dans le dictionnaire à partir des mots distants de 1 du mot de base
    word_distance1 = edits1(word)
    # sélection des seuls mots connus parmi cet ensemble
    known_word_distance1 = known(edits1(word))
    # si au moins un mot parmi cet ensemble est dans le dictionnaire
    if len(known_word_distance1) > 0:
        # retourne le mot qui a la probabilité maximum
        return max(known_word_distance1, key=probabilite)

    # ensemble des mots dans le dictionnaire à partir des mots distants de 2 du mot de base
    word_distance2 = edits2(word)
    # sélection des seuls mots connus parmi cet ensemble
    known_word_distance2 = known(word_distance2)
    # si au moins un mot parmi cet ensemble est dans le dictionnaire
    if len(known_word_distance2) > 0:
        # retourne le mot qui a la probabilité maximum
        return max(known_word_distance2, key=probabilite)

    # si aucun mot d'une distance de 2 ou moins n'a été trouvé, 
    return "not found"

def correctionInter(word): 
    '''
    Fonction qui, à partir d'un mot, détermine une liste des meilleures corrections possibles 
    s'il n'est pas dans le dictionnaire.
    '''

    global tree

    list_max = []

    # ensemble des mots dans le dictionnaire à partir des mots distants de 0 du mot de base
    word_distance0 = known([word])
    # si au moins un mot parmi cet ensemble est dans le dictionnaire
    if len(word_distance0) > 0:
        # retourne le mot qui a la probabilité maximum
        return max(word_distance0, key=probabilite)

    # ensemble des mots dans le dictionnaire à partir des mots distants de 1 du mot de base
    word_distance1 = edits1(word)
    # sélection des seuls mots connus parmi cet ensemble
    known_word_distance1 = known(edits1(word))
    # enregistrement d'une copie de cet ensemble pour la distance 2
    tmp = known(edits1(word))
    # si au moins un mot parmi cet ensemble est dans le dictionnaire
    if len(known_word_distance1) > 0:
        # tant qu'il reste des mots dans cet ensemble et que moins de 5 mots les plus probables ont été sélectionnés
        while known_word_distance1 != set() and len(list_max) < 5:
            # on ajoute à la liste le mot avec la probabilité maximum
            list_max.append(max(known_word_distance1, key=probabilite))
            # on enlève ce mot de l'ensemble des mots connus
            known_word_distance1.remove(max(known_word_distance1, key=probabilite))
        # si 5 mots les plus probables ont été sélectionnés, on retourne cette liste
        if len(list_max) == 5:
          return list_max

    # ensemble des mots dans le dictionnaire à partir des mots distants de 2 du mot de base
    word_distance2 = set(e2 for e1 in word_distance1 for e2 in edits1(e1))
    # sélection des seuls mots connus parmi cet ensemble
    known_word_distance2 = known(word_distance2)
    # si au moins un mot parmi cet ensemble est dans le dictionnaire
    if len(known_word_distance2) > 0:
        # tant qu'il reste des mots dans l'ensemble uniquement composé des mots de distance de 2 et que moins de 5 mots les plus probables ont été sélectionnés
        while known_word_distance2 ^ tmp != set() and len(list_max) < 5:
            # on ajoute à la liste le mot avec la probabilité maximum
            list_max.append(max(known_word_distance2 ^ tmp, key=probabilite))
            # on enlève ce mot de l'ensemble des mots connus
            known_word_distance2.remove(max(known_word_distance2 ^ tmp, key=probabilite))
        # on retourne la liste des mots sélectionnés
        return list_max

    # si au moins 1 mot a été sélectionnés dans l'ensemble des mots de distance 1
    if len(list_max) > 0:
        return list_max

    # si aucun mot d'une distance de 2 ou moins n'a été trouvé, 
    return "not found"
