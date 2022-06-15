import requests
import sys
from unicodedata import category

# enregistrement de l'arbre lexicographique
tree = requests.get("https://github.com/mducos/Correction-automatique/raw/main/production/structure_arborescente.json").json()

# récupération de tous les signes de ponctuation existant grâce à leur unicode car les catégories unicode P* sont destinées à la ponctuation
chrs = (chr(i) for i in range(sys.maxunicode + 1))
punctuation = set(c for c in chrs if category(c).startswith("P"))

def rechercheWordDict(word):
    '''
    Fonction qui prend un String en argument et renvoie un booléen, vrai si le String est présent 
    dans le dictionnaire, faux s’il n’y est pas. Pour cela, il faut que le mot comparé soit 
    totalement en minuscule (mais il ne faut pas que le mot lui-même ait été modifié). Si le 
    string est un signe de ponctuation, il n’est pas comparé.

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
    l'arbre si le mot y est présent. S'il l'est, cette fonction renvoie la fréquence du mot. 
    La fonction retourne un booléen.
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
    
