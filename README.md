# Correcteur orthographique

## Objectif

Implémenter un correcteur orthographique automatique et intéractif pour la langue française.

## Ressources utilisées

Le lexique utilisé est la dernière version au 10 février 2022 de http://www.lexique.org/ dont le manuel est https://github.com/mducos/Correcteur-orthographique/blob/main/ressources/Manuel_Lexique.3.pdf.
Les corpus de test et d'évaluation sont https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/corpus_fautes.txt et https://raw.githubusercontent.com/mducos/Correcteur-orthographique/main/ressources/corpus_corrige%CC%81.txt.

## Description des dossiers

### Ressources

Dossier où sont stockés les ressources utilisées, sans modifications postérieures, par le programme.

### Programmes

Dossier où sont stockés les fichiers python. Dans l'ordre d'exécution :
- structure_arborescente.py : programme pour construire l'arbre lexicographique à partir du lexique.
- création_fichiers_auxiliaires.py : programme pour enregistrer les listes des mots contenant un espace, une apostrophe ou un trait d'union.
- recherche_arbre.py : programme pour chercher un mot dans l'arbre lexicographique.
- detection_mots_fautifs.py : programme pour tokenizer un texte et détecter pour chaque mot rencontrer s'il est présent dans le lexique ou non. 
- algorithme_peter_norvig.py : programme pour générer tous les candidats d'une distance de 1 et 2 par rapport à un mot fautif et pour choisir le meilleur candidat parmi eux.
- correction_corpus.py : programme pour corriger entièrement un corpus textuel, que ce soit automatiquement ou intéractivement.
- evaluation.py : programme pour évaluer le correcteur orthographique automatique et intéractif.

Le programme est condensé dans un unique google collab : https://colab.research.google.com/drive/15KVB7cAmbWW3PLKfyX5Aqo5jdFCCXUsC?usp=sharing.

### Production

Dossier où sont stockés les fichiers produits par les programmes, notamment celui du corpus corrigé. Dans l'ordre de production :
- structure_arborescente.json : fichier où se trouve l'arbre lexicographique.
- two_words_in_one.json : fichier où se trouve la liste des mots contenant un espace.
- words_with_apostrophe.json : fichier où se trouve la liste des mots contenant une apostrophe.
- words_with_dash.json : fichier où se trouve la liste des mots contenant un trait d'union.
- corpus_corrigé_automatiquement.txt : fichier où est stockée la correction automatique.
- corpus_corrigé_intéractivement.txt : fichier où est stockée la correction intéractive.

## Pistes d'amélioration

Pistes d'amélioration pour diminuer le nombre de détections et de corrections en faux positifs (c’est-à-dire les mots détectés comme des erreurs puis corrigés alors qu’ils ne devraient pas l’être). Ces mots-là sont en fait des entités nommées, comme des noms de personne ou de lieu (dans le corpus de test, “Harry Potter” et “Poudlard” revenaient régulièrement). Par conséquent, pour éviter de corriger ces mots-là, il faudrait intégrer un programme de reconnaissance d’entités nommées pour ne pas les corriger (ou ne corriger que les noms d’organisation comme “Parlement”).

De plus, nous avons remarqué que la probabilité de chaque mot ne donne parfois pas la bonne correction. Un mot peut être suffisamment peu probable pour qu’un autre d’une même distance soit plus probable et soit choisi. Dans ce cas-là, nous pourrions privilégier certains types de fautes une fois que l’ensemble des corrections possibles est construit comme par exemple les inversions de deux lettres (les transpositions comme entre “maisno” et “maison”), les dédoublements de consonnes (comme entre “fraper” et “frapper”), les changements d’accents (comme “raclement” et “râclement”), ou encore

## Comment utiliser le programme

Bien que toutes les fonctions sont séparées dans le dossier **Programmes**, elles sont regroupées dans le fichier ... qu'il suffit de lancer pour corriger le texte mis dans la variable *corpus_pred*. Pour choisir soi-même le fichier texte à corriger, il suffit de changer son chemin d'accès.

