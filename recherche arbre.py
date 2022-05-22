import json

def recherche(tree_file, word):
    '''
    Fonction qui, à partir du fichier contenant l'arbre du vocabulaire
    et d'un mot, cherche dans l'arbre si le mot y est présent.
    La fonction retourne un booléen.
    "xylophone" → True
    "xylopone" → False
    '''

    # chargement du fichier
    tree = open(tree_file, "r", encoding="utf-8").readlines()
    # comme .readlines() crée un tableau, il faut prendre sa seule composante pour avoir le dictionnaire
    tree = tree[0]
    # conversion du dictionnaire à l'aide de json 
    tree = json.loads(tree)

    # on parcourt chaque lettre du mot pour vérifier qu'elles sont des noeuds/feuilles dans l'arbre
    return recherche_letter(tree, word)


def recherche_letter(tree, word):
    # cas de base : on lit la dernière lettre du mot
    if len(word) == 1:
        # la suite de lettres est dans l'arbre et la dernière lettre est finale donc c'est un mot du dictionnaire
        if "*" in tree[word]:
            return True
        # la suite de lettres est dans l'arbre mais la dernière lettre n'est pas finale donc ce n'est pas un mot du dictionnaire
        else:
            return False
    # si la première lettre est dans les clés du dictionnaire, on poursuit la recherche
    elif word[0] in tree:
        return recherche_letter(tree[word[0]], word[1:])
    # si elle n'y est pas, on peut dès à présent retourner faux
    else:
        return False

word = "xylophone"
print(recherche("C:/Users/carol/Desktop/L3/Projet_TAL/structure_arborescente.ttl", word))
