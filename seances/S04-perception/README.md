# S04 — Perception visuelle

## Objectif

Choisir le bon graphique pour une question donnée, et savoir justifier chaque choix d'encodage visuel.

## Prérequis

- [S03](../S03-semantique/README.md) terminée, et les tables `gold_trajets_horaires` et `gold_zones` présentes dans PostgreSQL (S02)
- `docker compose up -d`

## Apports

- Les variables visuelles : position, longueur, angle, aire, couleur
- La hiérarchie de perception de Cleveland et McGill (1984) : pourquoi la barre bat le camembert
- Partir de la question : comparer, montrer une évolution, une répartition, une relation, une géographie
- La couleur : palettes séquentielles, divergentes, catégorielles ; pourquoi bannir l'arc-en-ciel
- Le titre qui énonce la conclusion, les axes qui portent des unités

## Démonstration

Notebook **`04_perception.ipynb`** : l'expérience camembert contre barres, puis trois graphiques ratés construits sur nos données.

## À vous de jouer

1. **Atelier « makeover »** (en équipe) : pour chacun des graphiques A, B et C du notebook, écrivez la question visée,
   listez ce qui ne va pas, puis refaites-le en justifiant chaque choix.
2. **Choisir le graphique** : répondez aux trois questions de la partie 3 du notebook, avec un titre qui énonce la conclusion.
3. **Revue croisée** : échangez vos versions avec une autre équipe. Chaque équipe relève un point fort et un point à améliorer.

## C'est réussi quand…

- les trois graphiques refaits répondent chacun à une question explicite ;
- aucun axe de barres ne commence ailleurs qu'à zéro ;
- chaque couleur a un sens, ou n'est pas utilisée ;
- chaque titre énonce une conclusion.

## Dépôt pour le dossier MSPR 4.1

Les trois « avant / après » commentés, et vos trois graphiques de la partie 3.

## Nettoyage

```bash
docker compose stop
```

## Séance suivante

[S05 — Visualisation en code](../S05-viz-code/README.md)
