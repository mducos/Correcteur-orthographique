# 1. PRISE EN MAIN DES RESSOURCES

  # 1) LECTURE DU CORPUS
  
import requests

corpus_pred = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/corpus_fautes.txt").text
corpus_gold = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/corpus_corrige%CC%81.txt").text

  # 2) INITIALISATION DES VARIABLES GLOBALES
  
import requests
import json
import sys
from unicodedata import category
import re

# lecture du dictionnaire sous format tsv 
lines = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/Lexique383.tsv").text.split("\n")

# enregistrement des ensembles de mots particuliers
wordsWithApostrophe = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/production/words_with_apostrophe.json").json()
wordsWithSpace = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/production/two_words_in_one.json").json()
wordsWithDash = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/production/words_with_dash.json").json()

# enregistrement de l'arbre lexicographique
tree = requests.get("https://github.com/mducos/Correction-automatique/raw/main/production/structure_arborescente.json").json()

# corpus corrigés par le programme
corpus_auto = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/production/corpus_corrig%C3%A9_automatiquement.txt").text
corpus_inter = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/production/corpus_corrig%C3%A9_int%C3%A9ractivement.txt").text

# récupération de tous les signes de ponctuation existant grâce à leur unicode car les catégories unicode P* sont destinées à la ponctuation
chrs = (chr(i) for i in range(sys.maxunicode + 1))
punctuation = set(c for c in chrs if category(c).startswith("P"))

  # 3) CONSTRUCTION DE L'ARBRE LEXICOGRAPHIQUE

def vocab2tree():

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

      
      
# 2. CONSTRUCTION DES FONCTIONS AUXILIAIRES DE RECHERCHE

def twoWordsInOne():

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

  
  
# 3. IMPLEMENTATION DE L'ALGORITHME DE PETER NORVIG ADAPTE
  
def edits1(word):

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

    # retourne l'ensemble de tous les mots générés avec une distance de 1 avec les mots générés avec une distance de 1
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))
  
def known(words): 

    global tree
    # retourne l'ensemble des mots qui existe dans l'arbre lexicographique
    return set(w for w in words if rechercheWordRec(tree, w))

def probabilite(word):

    global tree
    
    return frequence_relative(tree, word) 

def frequence_relative(tree, word):
    
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
  
  
  
# 4. ALGORITHME DE RECONNAISSANCE DES MOTS FAUTIFS

def addSpace(str):
  
    global punctuation

    # on parcourt tous les caractères du string
    for char in str:
        # si le charactère est un signe de ponctuation
        if char in punctuation:
            # les mots contenant un - seront traités plus tard
            if char != "-":
                # on entoure ce caractère d'un espace
                str = str.replace(char, " " + char + " ")
    
    return str
  
def corpusToList(corpus):

    global wordsWithDash
    global woredsWithSpace
    global wordsWithApostrophe

    # pour chaque mot de l'ensemble des mots avec une apostrophe de plus de 2 caractères (pour enlever les "l'" et "d'"), on vérifie s'il est dans le corpus
    for word in wordsWithApostrophe:
        if word in corpus.lower() and len(word) > 2:
            # s'il y est, on change l'apostrophe en un signe présent dans aucun mot pour pouvoir le reconnaître plus tard
            corpus = corpus.replace(word, word.replace("'", "$"))
            # mais si le mot a une majuscule au début, il faut le traiter ainsi
            word = word[0].upper() + word[1:]
            corpus = corpus.replace(word, word.replace("'", "$"))

    # ajout des espaces autour des signes de ponctuation
    corpus = addSpace(corpus)

    # pour chaque mot de l'ensemble des mots à 2 composés, on vérifie s'il est dans le corpus
    for word in wordsWithSpace:
        # on doit faire comme si les apostrophes étaient sous forme d'apostrophe
        if word in corpus.replace("$", "'").lower():
            # s'il y est, on change l'espace en un signe présent dans aucun mot pour pouvoir le reconnaître plus tard
            corpus = corpus.replace(word.replace("'", "$"), word.replace("'", "$").replace(" ", "*"))
            # mais si le mot a une majuscule au début, il faut le traiter ainsi
            word = word[0].upper() + word[1:]
            corpus = corpus.replace(word.replace("'", "$"), word.replace("'", "$").replace(" ", "*"))

    # en splitant, les composants d'un mot qui contient originellement un espace ne sont plus séparés
    corpus = corpus.split()
    # pour chaque mot du corpus
    for i in range(len(corpus)):
        # s'il contient * signifie que c'est un mot à plusieurs composants
        if "$" in corpus[i]:
            # on remet l'espace
            corpus[i] = corpus[i].replace("$", "'")
        # s'il contient * signifie que c'est un mot à plusieurs composants
        if "*" in corpus[i]:
            # on remet l'espace
            corpus[i] = corpus[i].replace("*", " ")
    
    # pour chaque mot du corpus
    for i in range(len(corpus)):
        # s'il contient un tiret
        if "-" in corpus[i]:
            # on vérifie qu'il ne fait pas partie de l'ensemble des mots à tiret
            if not(corpus[i].lower() in wordsWithDash):
                # on ajoute les espaces nécessaires autour de la ponctuation
                corpus[i] = corpus[i].replace("-", " - ")
                # on transforme l'expression en liste
                listWord = corpus[i].split()
                # on supprime le faux mot avec tiret dans le corpus
                del corpus[i]
                # et on ajoute à l'indice i tous les mots de la liste
                for component in reversed(listWord):
                    corpus.insert(i, component)

    return corpus  

def rechercheWordDict(word):
  
    global tree
    global punctuation

    # si le mot n'est pas un signe de ponctuation
    if not(word in punctuation):
        # on parcourt chaque lettre du mot pour vérifier qu'elles sont des noeuds/feuilles dans l'arbre
        return rechercheWordRec(tree, word.lower())
        
def rechercheWordRec(tree, word):

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
        
        
        
# 5. IMPLEMENTATION DE LA CORRECTION DU CORPUS

def typeOfCorrection():

    # initialisation de la variable
    typeCorrection = ""
    # tant que l'utilisateur n'a pas répondu correctement à la question, celle-ci est reposée
    while typeCorrection == "":
        # question posée pour déterminer si la correction sera automatique ou intéractive
        answer = input("Quel type de correction voulez-vous ? 'automatique' ou 'intéractif' ?\n")
        # si la réponse donnée par l'utilisateur est "automatique" ou "intéractif"
        if answer == "automatique" or answer == "intéractif":
            # on stocke cette réponse
            typeCorrection = answer

    return typeCorrection

def correctionAutomatique():

    global corpus_pred
    # séparation du corpus en paragraphe
    corpus_pred = corpus_pred.split("\n")

    corrected_sentence = ""
    # pour chaque ligne du corpus
    for line in corpus_pred :
        # on tokenize la ligne
        tokenized_list = (corpusToList(line))

        # pour chaque élément dans cette liste tokenisée
        for elt in tokenized_list:
            # si le mot n'existe pas
            if rechercheWordDict(elt) == False:
                # enregistrement de la forme juste la plus probable du mot fautif
                corrected = correctionAuto(elt.lower())
                # si la forme juste la plus probable n'a pas été trouvée
                if corrected == "not found":
                    # on réécrit le mot tel quel
                    corrected_sentence = corrected_sentence + " " + elt
                # si une forme juste la plus probable a été trouvée
                else:
                    # pour chaque lettre dans le mot
                    for letter_id in range(len(min(corrected, elt, key=len))):
                        # si une majuscule était présente dans la phrase d'origine
                        if elt[letter_id] == elt[letter_id].upper():
                            # on modifie le mot juste en y ajoutant la majuscule sur la bonne lettre
                            corrected = corrected.replace(corrected[letter_id], corrected[letter_id].upper())
                    # on écrit le mot corrigé dans le fichier
                    corrected_sentence = corrected_sentence + " " + corrected
            # si le mot existe
            else:
                # on le réécrit dans le fichier
                corrected_sentence = corrected_sentence + " " + elt

        # à chaque changement de paragraphe (ie line), on ajoute un saut de ligne
        corrected_sentence = corrected_sentence + "\n"

    # on enlève tous les espaces superflus dus à addSpace()
    corrected_sentence = re.sub(r'\s+([.,\"])', r'\1', corrected_sentence)
    corrected_sentence = re.sub(r"\s+([-'])\s", r'\1', corrected_sentence)
    return corrected_sentence
    
def correctionInteractive():
  
    global corpus_pred
    # séparation du corpus en paragraphe
    corpus_pred = corpus_pred.split("\n")

    corrected_sentence = ""
    # pour chaque ligne dans ce fichier
    for line in corpus_pred:
        # on tokenize la ligne
        tokenized_list = (corpusToList(line))
        # pour chaque élément dans cette liste tokenisée
        for id, elt in enumerate(tokenized_list):
            # si le mot n'existe pas
            if rechercheWordDict(elt) == False:
                # enregistrement de la forme juste la plus probable du mot fautif
                corrected = correctionInter(elt.lower())
                # si aucune forme juste n'a été trouvée
                if corrected == "not found":
                    # on réécrit le mot tel quel dans le fichier
                    corrected_sentence = corrected_sentence +" " + elt
                # si une liste de formes justes a été trouvée
                else:
                    proposition = '"' + '", "'.join([w for w in corrected])
                    best_word = ""
                    # tant que l'utilisateur n'a pas répondu correctement à la question, celle-ci est reposée
                    while best_word == "":
                        # question posée pour déterminer si la correction sera automatique ou intéractive
                        answer = input("\nMot inconnu : " + elt + "\ndans le contexte : " + tokenized_list[id-1] + " " + elt + " " + tokenized_list[id+1] + "\nVeuillez choisir une correction possible : " + proposition + '", "not found"' + "\n")
                        # si la réponse correspond à un des mots proposés, on stocke le mot choisi
                        if answer in proposition.split('"'):
                            best_word = answer
                            answer = "_"
                        elif answer == "not found":
                            best_word = elt
                    # pour chaque lettre dans le mot
                    for letter_id in range(len(min(best_word, elt, key=len))):
                        # si une majuscule était présente dans la phrase d'origine
                        if elt[letter_id] == elt[letter_id].upper():
                            # on modifie le mot juste en y ajoutant la majuscule sur la bonne lettre
                            best_word = best_word.replace(best_word[letter_id], best_word[letter_id].upper())
                    # on écrit le mot corrigé dans le fichier
                    corrected_sentence = corrected_sentence + " " + best_word

            # si le mot existe
            else:
                # on le réécrit dans le fichier
                corrected_sentence = corrected_sentence + " " + elt
            
        # à chaque changement de paragraphe (ie line), on ajoute un saut de ligne
        corrected_sentence = corrected_sentence + "\n"
        
    # on enlève tous les espaces superflus dus à addSpace()
    corrected_sentence = re.sub(r'\s+([.,\"])', r'\1', corrected_sentence)
    corrected_sentence = re.sub(r"\s+([-'])\s", r'\1', corrected_sentence)
    return corrected_sentence

# choix du type de correction
typeCorrection = typeOfCorrection()

if typeCorrection == "automatique":
    print(correctionAutomatique())
elif typeCorrection == "intéractif":
    print(correctionInteractive())  
    
