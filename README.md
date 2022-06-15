# Stage de L3

## Objectif

Tâche de projection de lexique sur corpus :

Identification des occurrences en corpus d'unités lexicales définies dans le lexique issu de wiktionary sans faire de désambiguisation.

## Ressources utilisées

Le dictionnaire des lemmes et des multi-word-expressions provient de la version ontolex_20220301 du wiktionnary.

Le corpus de test est sequoia.deep_and_surf.parseme.frsemcor.



## Description des dossiers

### Ressources

Dossier où sont stockés les fichiers utilisés, sans modifications postérieures, par le programme.

### Programmes

Dossier où sont stockés les fichiers python.
- filtrage_wiktionnary_20220301.py : pour filtrer le fichier ttl ontolex_20220301 de wiktionnary selon diverses options à choisir
- extraction_json_mwe_20220301.py : extraction des multi-word-expressions en un dictionnaire
- extraction_json_single_words_20220301.py : extraction des lemmes simples en un dictionnaire
- projection_wiktionnary_20220301.py : première partie de la projection des lemmes simples et des mwe sur le corpus sequoia
- projection_wiktionnary_20220301_post-traitement.py : deuxième partie de la projection en retirant les mwe qui se superposent
- projection_sequoia_parseme_evaluation.py : ajout de l'annotation du sequoia pour faire l'évaluation des programmes

### Production

Dossier où sont stockés les fichiers produits par les programmes, notamment celui de projection du lexique sur le corpus.

## Difficultés rencontrées

Liste des problèmes rencontrés concernant la façon dont le fichier ontolex_20220301 de wiktionnary a été construit :
- s’apercevoir/s’avérer : la version pronominal "s'apercevoir"/"s'avérer" est un sens (avec exemples) dans la version non pronominale "apercevoir"/"avérer", en plus d'être un LexicalEntry à part sans exemple ou avec d'autres exemples
- certains LVC sont présents dans wiktionnary en tant que LexicalEntry, mais d'autres non

## Comment utiliser le programme
