import requests

corpus_pred = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/corpus_fautes.txt").text
corpus_gold = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/corpus_corrige%CC%81.txt").text

# corpus corrigés par le programme
corpus_auto = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/production/corpus_corrig%C3%A9_automatiquement.txt").text
corpus_inter = requests.get("https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/production/corpus_corrig%C3%A9_int%C3%A9ractivement.txt").text

def evaluation_correction_automatique():

    global corpus_gold
    global corpus_auto
    global corpus_pred

    # tokenization simple des différents corpus
    gold_tokens = addSpace(corpus_gold).split()
    auto_tokens = addSpace(corpus_auto).split()
    origine_tokens = addSpace(corpus_pred).split()

    # variables pour la correction des mots fautifs
    faux_negatif = 0 # mot fautif non corrigé
    faux_positif = 0 # mot fautif mal corrigé
    vrai_positif = 0 # mot fautif bien corrigé
    vrai_negatif = 0 # mot non-fautif non corrigé

    # variables pour la détection des mots fautifs
    vraie_erreur_detectee = 0 # erreurs détectées
    vraie_erreur_non_detectee = 0 # erreurs non détectées
    fausse_erreur_detectee = 0 # erreurs détectées qui ne sont pas une erreur
    vraie_erreur_detectee_non_corrigee = 0 # erreurs détectées dont aucune correction n'a été trouvée

    # pour chaque mot dans le corpus corrigé automatiquement
    for i in range(len(auto_tokens)):
        # si ce mot est le même dans le corpus corrigé mais qu'il est différent de celui d'origine
        if auto_tokens[i] == gold_tokens[i] and auto_tokens[i] != origine_tokens[i]:
            # cela signifie que le mot a été corrigé correctement
            vrai_positif += 1
        # si ce mot est le même dans le corpus corrigé et dans le corpus d'origine
        elif auto_tokens[i] == gold_tokens[i] and auto_tokens[i] == origine_tokens[i]:
            # cela signifie que ce mot était déjà juste
            vrai_negatif += 1
        # si ce mot est différent de celui dans le corpus corrigé et différent de celui dans le corpus d'origine
        elif auto_tokens[i] != gold_tokens[i] and auto_tokens[i] != origine_tokens[i]:
            # cela signifie que le mot a été corrigé mais avec une mauvaise correction
            faux_positif += 1
        # si ce mot est différent de celui dans le corpus corrigé et est le même de celui du corpus d'origine
        elif auto_tokens[i] != gold_tokens[i] and auto_tokens[i] == origine_tokens[i]:
            # cela signifie que le mot n'a pas été corrigé alors qu'il aurait dû
            faux_negatif += 1


        # si ce mot est différent de celui d'origine, que l'algo n'a pas changé le mot d'origine alors que celui-ci n'existe pas
        if gold_tokens[i] != origine_tokens[i] and auto_tokens[i] == origine_tokens[i] and known([origine_tokens[i]]) == set():
            # cela signifie que l'erreur a été détectée mais aucune correction n'a été trouvée
            vraie_erreur_detectee_non_corrigee += 1
        # si ce mot est différent de celui d'origine, que l'algo n'a pas changé le mot d'origine alors que celui-ci existe
        elif gold_tokens[i] != origine_tokens[i] and auto_tokens[i] == origine_tokens[i] and known([origine_tokens[i]]) != set():
            # cela signifie que l'algorithme n'a pas détecté d'erreur
            vraie_erreur_non_detectee += 1
        # si ce mot est différent de celui d'origine et que l'algo a également changé le mot d'origine
        elif gold_tokens[i] != origine_tokens[i] and auto_tokens[i] != origine_tokens[i]:
            # cela signifie que le mot fautif a bien été détecté
            vraie_erreur_detectee += 1
        # si ce mot est le même que celui d'origine alors que l'algo a changé le mot d'origine
        elif gold_tokens[i] == origine_tokens[i] and auto_tokens[i] != origine_tokens[i]:
            # cela signifie que le mot est reconnu comme fautif alors qu'il est correct
            fausse_erreur_detectee += 1
            
    # calcul de la précision, du rappel et du fscore de la correction
    precision = vrai_positif/(vrai_positif + faux_positif)
    rappel = vrai_positif/(vrai_positif + faux_negatif)
    pourc_fscore = "{0:.0%}".format(2*rappel*precision/(rappel + precision))
    pourc_rappel = "{0:.0%}".format(rappel)
    pourc_precision = "{0:.0%}".format(precision)

    print(f"CORRECTION :\n# vrai positif : {vrai_positif} ;\n# faux positif : {faux_positif} ;\n# vrai négatif : {vrai_negatif} ;\n# faux négatif : {faux_negatif} ;\n# rappel : {pourc_rappel} ;\n# précision : {pourc_precision} ;\n# fscore : {pourc_fscore} ;\n")

    # calcul de la précision, du rappel et du fscore de la détection
    precision = (vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee)/(vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee + fausse_erreur_detectee)
    rappel = (vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee)/(vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee + vraie_erreur_non_detectee)
    pourc_fscore = "{0:.0%}".format(2*rappel*precision/(rappel + precision))
    pourc_rappel = "{0:.0%}".format(rappel)
    pourc_precision = "{0:.0%}".format(precision)

    print(f"DETECTION :\n# vrai positif : {vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee} ;\n# faux positif : {fausse_erreur_detectee} ;\n# vrai négatif : {len(auto_tokens) - (vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee + fausse_erreur_detectee + vraie_erreur_non_detectee)} ;\n# faux négatif : {vraie_erreur_non_detectee} ;\n# rappel : {pourc_rappel} ;\n# précision : {pourc_precision} ;\n# fscore : {pourc_fscore} ;")

def evaluation_correction_interactive():

    global corpus_gold
    global corpus_inter
    global corpus_pred

    # tokenization simple des différents corpus
    gold_tokens = addSpace(corpus_gold).split()
    inter_tokens = addSpace(corpus_inter).split()
    origine_tokens = addSpace(corpus_pred).split()

    # variables pour la correction des mots fautifs
    faux_negatif = 0 # mot fautif non corrigé
    faux_positif = 0 # mot fautif mal corrigé
    vrai_positif = 0 # mot fautif bien corrigé
    vrai_negatif = 0 # mot non-fautif non corrigé

    # variables pour la détection des mots fautifs
    vraie_erreur_detectee = 0 # erreurs détectées
    vraie_erreur_non_detectee = 0 # erreurs non détectées
    fausse_erreur_detectee = 0 # erreurs détectées qui ne sont pas une erreur
    vraie_erreur_detectee_non_corrigee = 0 # erreurs détectées dont aucune correction n'a été trouvée

    # pour chaque mot dans le corpus corrigé intéractivement
    for i in range(len(inter_tokens)):
        # si ce mot est le même dans le corpus corrigé mais qu'il est différent de celui d'origine
        if inter_tokens[i] == gold_tokens[i] and inter_tokens[i] != origine_tokens[i]:
            # cela signifie que le mot a été corrigé correctement
            vrai_positif += 1
        # si ce mot est le même dans le corpus corrigé et dans le corpus d'origine
        elif inter_tokens[i] == gold_tokens[i] and inter_tokens[i] == origine_tokens[i]:
            # cela signifie que ce mot était déjà juste
            vrai_negatif += 1
        # si ce mot est différent de celui dans le corpus corrigé et différent de celui dans le corpus d'origine
        elif inter_tokens[i] != gold_tokens[i] and inter_tokens[i] != origine_tokens[i]:
            # cela signifie que le mot a été corrigé mais avec une mauvaise correction
            faux_positif += 1
            print(gold_tokens[i], inter_tokens[i], origine_tokens[i])
        # si ce mot est différent de celui dans le corpus corrigé et est le même de celui du corpus d'origine
        elif inter_tokens[i] != gold_tokens[i] and inter_tokens[i] == origine_tokens[i]:
            # cela signifie que le mot n'a pas été corrigé alors qu'il aurait dû
            faux_negatif += 1

        # si ce mot est différent de celui d'origine, que l'algo n'a pas changé le mot d'origine alors que celui-ci n'existe pas
        if gold_tokens[i] != origine_tokens[i] and inter_tokens[i] == origine_tokens[i] and known([origine_tokens[i]]) == set():
            # cela signifie que l'erreur a été détectée mais aucune correction n'a été trouvée
            vraie_erreur_detectee_non_corrigee += 1
        # si ce mot est différent de celui d'origine, que l'algo n'a pas changé le mot d'origine alors que celui-ci existe
        elif gold_tokens[i] != origine_tokens[i] and inter_tokens[i] == origine_tokens[i] and known([origine_tokens[i]]) != set():
            # cela signifie que l'algorithme n'a pas détecté d'erreur
            vraie_erreur_non_detectee += 1
        # si ce mot est différent de celui d'origine et que l'algo a également changé le mot d'origine
        elif gold_tokens[i] != origine_tokens[i] and inter_tokens[i] != origine_tokens[i]:
            # cela signifie que le mot fautif a bien été détecté
            vraie_erreur_detectee += 1
        # si ce mot est le même que celui d'origine alors que l'algo a changé le mot d'origine
        elif gold_tokens[i] == origine_tokens[i] and inter_tokens[i] != origine_tokens[i]:
            # cela signifie que le mot est reconnu comme fautif alors qu'il est correct
            fausse_erreur_detectee += 1

    # calcul de la précision, du rappel et du fscore de la correction
    precision = vrai_positif/(vrai_positif + faux_positif)
    rappel = vrai_positif/(vrai_positif + faux_negatif)
    pourc_fscore = "{0:.0%}".format(2*rappel*precision/(rappel + precision))
    pourc_rappel = "{0:.0%}".format(rappel)
    pourc_precision = "{0:.0%}".format(precision)

    print(f"CORRECTION :\n# vrai positif : {vrai_positif} ;\n# faux positif : {faux_positif} ;\n# vrai négatif : {vrai_negatif} ;\n# faux négatif : {faux_negatif} ;\n# rappel : {pourc_rappel} ;\n# précision : {pourc_precision} ;\n# fscore : {pourc_fscore} ;\n")

    # calcul de la précision, du rappel et du fscore de la détection
    precision = (vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee)/(vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee + fausse_erreur_detectee)
    rappel = (vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee)/(vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee + vraie_erreur_non_detectee)
    pourc_fscore = "{0:.0%}".format(2*rappel*precision/(rappel + precision))
    pourc_rappel = "{0:.0%}".format(rappel)
    pourc_precision = "{0:.0%}".format(precision)

    print(f"DETECTION :\n# vrai positif : {vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee} ;\n# faux positif : {fausse_erreur_detectee} ;\n# vrai négatif : {len(inter_tokens) - (vraie_erreur_detectee + vraie_erreur_detectee_non_corrigee + fausse_erreur_detectee + vraie_erreur_non_detectee)} ;\n# faux négatif : {vraie_erreur_non_detectee} ;\n# rappel : {pourc_rappel} ;\n# précision : {pourc_precision} ;\n# fscore : {pourc_fscore} ;")

