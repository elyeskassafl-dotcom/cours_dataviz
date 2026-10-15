# S03 — Sémantique : RDF, OWL, SPARQL

## Objectif

Donner du sens à nos données : décrire le domaine NYC Taxi avec une ontologie, l'interroger en SPARQL,
la relier à Wikidata et visualiser le graphe de connaissances obtenu.

## Prérequis

- [S02](../S02-preparation-spark/README.md) terminée
- `docker compose up -d`
- Les fichiers `data/raw/taxi_zone_lookup.csv` et `data/raw/yellow_tripdata_2025-01.parquet` sont présents

## Apports

- **RDF** : toute information s'écrit sous forme de triplets *sujet → prédicat → objet*, chaque élément ayant une URI unique.
- **OWL** : on déclare des classes, des relations et des hiérarchies. Une `ZoneAeroport` est une `Zone`.
- **SPARQL** : on interroge un graphe en décrivant le motif de triplets recherché, avec filtres et agrégats comme en SQL.
- **Interopérabilité** : `owl:sameAs` relie nos entités à des référentiels publics (Wikidata), sans table de correspondance.
- **Catalogage et lignage** : savoir d'où vient chaque donnée et qui l'utilise (Apache Atlas, en démonstration).

## Démonstration

**Modéliser** l'ontologie dans **Protégé**, l'éditeur d'ontologies de l'université de Stanford (https://protege.stanford.edu),
puis l'**interroger** dans **Apache Jena Fuseki**, un serveur SPARQL avec interface web :

```bash
docker compose --profile semantique up -d
```

puis http://localhost:3030 (`admin` / `admin`) : dataset `ds` → *add data* → `graphe_nyctaxi.ttl` → onglet *query*.

Ensuite, le notebook **`03_rdf_sparql.ipynb`** :

1. Construction de l'ontologie (classes, relations, attributs) et lecture au format Turtle
2. Chargement des zones de taxi, des arrondissements, des modes de paiement et d'un échantillon de 300 courses
3. Trois requêtes SPARQL : zones de Manhattan, zones par arrondissement, courses au départ des aéroports
4. Lien vers Wikidata avec `owl:sameAs`
5. Export de l'ontologie et du graphe (`.ttl`), puis graphe interactif (`graphe_zones.html`)

## À vous de jouer

1. Faites les trois exercices de fin de notebook.
2. Enrichissez l'ontologie avec **une notion de votre choix** utile au responsable d'exploitation
   (tranche horaire, type de tarif, zone touristique…) et justifiez-la en deux phrases.
3. Écrivez **une requête SPARQL** qui répond à une question métier et que vous n'auriez pas pu écrire aussi simplement en SQL
   sur les tables *gold*. Expliquez pourquoi.
4. Question de réflexion : *pourquoi ne pas mettre les 3 millions de courses dans le graphe ?*

## C'est réussi quand…

- l'ontologie se charge sans erreur et le graphe contient toutes les zones de taxi de New York ;
- la requête « zones de Manhattan » renvoie un résultat ;
- `graphe_zones.html` s'ouvre dans le navigateur ;
- votre enrichissement d'ontologie est justifié.

## Dépôt pour le dossier MSPR 4.1

`ontologie_nyctaxi.ttl` + vos requêtes SPARQL commentées + une capture du graphe + la justification de votre enrichissement.

## Nettoyage

```bash
docker compose stop
```

## Séance suivante

[S04 — Perception visuelle](../S04-perception/README.md)
