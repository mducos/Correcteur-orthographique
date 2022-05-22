import numpy as np

def distance_damerau_levenshtein(s1, s2):
    '''
    Fonction qui, à partir de deux mots s1 et s2, calcule la distance
    de Damerau-Levenshtein et renvoie ce nombre.
    "chien", "niche" → 4
    "maison", "maisno" → 1

    Cette fonction crée une matrice calculant la distance de Damerau-
    Levenshtein des deux mots au fur et à mesure de leur lecture.
           n  i  c  h  e
      [[0. 1. 2. 3. 4. 5.]
    n  [1. 0. 1. 2. 3. 4.]
    i  [2. 1. 0. 1. 2. 3.]
    e  [3. 2. 1. 1. 2. 2.]
    r  [4. 3. 2. 2. 2. 3.]]
    La distance entre ces deux mots est la case [len(s1), len(s2)],
    c'est-à-dire la case en bas à droite.
    '''

    # simplification des variables. Le +1 correspond à la ligne et la colonne supplémentaire de la matrice
    lenstr1 = len(s1) +1
    lenstr2 = len(s2) +1

    # création de la matrice
    levenshtein_matrix = np.zeros((lenstr1, lenstr2))

    # calcul de la distance en comparant s1 à un mot vide pour remplir la première colonne
    for i in range(lenstr1):
        # étant donné le mot vide, la distance sera forcément la longueur comparée de s1
        levenshtein_matrix[i,0] = i
    # calcul de la distance en comparant s2 à un mot vide pour remplir la première ligne
    for j in range(lenstr2):
        # étant donné le mot vide, la distance sera forcément la longueur comparée de s2
        levenshtein_matrix[0,j] = j

    # pour le coeur de la matrice, il faut comparer tous les débuts possibles de s1 avec tous les débuts possibles de s2
    for i in range(1, lenstr1):
        for j in range(1, lenstr2):

            # le coût est nul si les deux lettres aux mêmes indices sont les mêmes (car pas d'opération nécessaire)
            if s1[i-1] == s2[j-1]:
                cost = 0
            # si ces deux lettres ne sont pas identiques, il faut effectuer une opération. Comme elles coûtent toute 1, le coût est de 1
            else:
                cost = 1

            # la distance correspond au minimum de la somme de la distance précédente à laquelle on ajoute le coût pour une des opérations possibles
            levenshtein_matrix[i,j] = min(
                    # suppression
                    levenshtein_matrix[i-1, j] +1,
                    # insertion
                    levenshtein_matrix[i, j-1] +1,
                    # substitution
                    levenshtein_matrix[i-1, j-1] + cost
                )
            # dans le cas où les deux indices sont les mêmes et que leurs lettres respectives correspondent l'une à l'autre à 1 indice près, l'opération est une transposition
            if i == j and s1[i-1] == s2[j-2] and s1[i-2] == s2[j-1]:
                # la distance correspond au minimum entre la distance précédemment calculée et la distance calculée avant le phénomène de transposition entre les deux mots
                levenshtein_matrix[i,j] = min (
                    levenshtein_matrix[i,j], 
                    levenshtein_matrix[i-3,j-3] + cost
                )

    # on retourne la dernière case de la matrice, symbolisant la distance
    return levenshtein_matrix[lenstr1-1, lenstr2-1]


print(distance_damerau_levenshtein("maison", "maisno"))
