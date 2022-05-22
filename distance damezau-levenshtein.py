import numpy as np

def distance_damerau_levenshtein(s1, s2):
    '''
    Fonction qui, à partir de deux mots s1 et s2, calcule la distance
    de Damerau-Levenshtein et renvoie ce nombre.
    "chien", "niche" → 4
    "maison", "maisno" → 1

    Cette fonction crée une matrice calculant la distance de Damerau-
    Levenshtein des deux mots au fur et à mesure de leur lecture.
        n   i   c   h   e
      [[0. 1. 2. 3. 4. 5.]
    n  [1. 0. 1. 2. 3. 4.]
    i  [2. 1. 0. 1. 2. 3.]
    e  [3. 2. 1. 1. 2. 2.]
    r  [4. 3. 2. 2. 2. 3.]]
    La distance entre ces deux mots est la case [len(s1), len(s2)],
    c'est-à-dire la case en bas à droite.
    '''

    lenstr1 = len(s1) +1
    lenstr2 = len(s2) +1
    levenshtein_matrix = np.zeros((lenstr1, lenstr2))

    for i in range(lenstr1):
        levenshtein_matrix[i,0] = i
    for j in range(lenstr2):
        levenshtein_matrix[0,j] = j

    for i in range(1, lenstr1):
        for j in range(1, lenstr2):
            if s1[i-1] == s2[j-1]:
                cost = 0
            else:
                cost = 1
            levenshtein_matrix[i,j] = min(
                    levenshtein_matrix[i-1, j] +1,
                    levenshtein_matrix[i, j-1] +1,
                    levenshtein_matrix[i-1, j-1] + cost
                )
            if i == j and s1[i-1] == s2[j-2] and s1[i-2] == s2[j-1]:
                levenshtein_matrix[i,j] = min (
                    levenshtein_matrix[i,j], 
                    levenshtein_matrix[i-3,j-3] + cost
                )

    print(levenshtein_matrix)
    return levenshtein_matrix[lenstr1-1, lenstr2-1]


print(distance_damerau_levenshtein("maison", "maisno"))