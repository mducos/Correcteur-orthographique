import json

# chargement du dictionnaire
tree = open("C:/Users/carol/Desktop/L3/Projet_TAL/structure_arborescente.ttl", "r", encoding="utf-8").readlines()
tree = tree[0]
tree = json.loads(tree)

def edits1(word):
    "All edits that are one edit away from `word`."

    letters    = 'abcdefghijklmnopqrstuvwxyzàâæçéèêëîïôœùûüÿ'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    # retourne l'ensemble de tous les mots générés avec une distance de 1 avec les mots générés avec une distance de 1
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits3(word): 
    # retourne l'ensemble de tous les mots générés avec une distance de 1 avec les mots générés avec une distance de 1 avec les mots générés avec une distance de 1
    return set(e3 for e1 in edits1(word) for e2 in edits1(e1) for e3 in edits1(e2))

def known(words): 
    global tree
    # retourne l'ensemble des mots qui existe dans l'arbre lexicographique
    return set(w for w in words if recherche_letter(tree, w))

def recherche_letter(tree, word):
    # cas de base : on lit la dernière lettre du mot
    if len(word) == 1:
        # si la suite de lettres est dans l'arbre mais la dernière lettre n'y est pas donc ce n'est pas un mot du dictionnaire
        if not(word in tree):
            return False
        # si la suite de lettres est dans l'arbre et la dernière lettre est finale donc c'est un mot du dictionnaire
        if "*" in tree[word]:
            return True
        # si la suite de lettres est dans l'arbre mais la dernière lettre n'est pas finale donc ce n'est pas un mot du dictionnaire
        else:
            return False
    # si la première lettre est dans les clés du dictionnaire, on poursuit la recherche
    elif word[0] in tree:
        return recherche_letter(tree[word[0]], word[1:])
    # si elle n'y est pas, on peut dès à présent retourner faux
    else:
        return False


# série de test avec le mot pour obtenir "maison"
print(len(edits1("maiso")))
print(len(edits2("maiso"))) # instantannée donc c'est ok pour le temps
#print(len(edits3("maiso"))) # beaucoup trop long : de l'ordre de la minute
print(len(known(edits1("maiso"))))
print(len(known(edits2("maiso"))))
print(known(edits2("maiso")))
#print(known(edits3("maiso"))) # beaucoup trop long : de l'ordre de la minute
