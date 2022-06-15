import requests

corpus_pred = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/corpus_fautes.txt").text

def typeOfCorrection():
    '''
    Fonction de départ qui demande à l'utilisateur quel type de correction il souhaite entre une 
    correction automatique et une correction intéractive.

    Cette fonction lance toutes les suivantes pour effectuer la correction souhaitée, et retourne 
    le corpus corrigé.
    '''

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
    
