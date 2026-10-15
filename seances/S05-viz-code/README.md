# S05 — Visualisation en code : Plotly, Altair, Streamlit

## Objectif

Passer de graphiques figés à une application d'analyse interactive : carte des zones, courbes, filtres,
le tout conteneurisé avec Docker.

## Prérequis

- [S04](../S04-perception/README.md) terminée
- `docker compose up -d`
- Le fichier `data/raw/taxi_zones.zip` est présent (téléchargé par `scripts/telecharger_donnees.sh`)

## Apports

- Plotly Express : un graphique interactif en une ligne
- Altair et la grammaire graphique : marques, encodages, vues liées
- Données géographiques : shapefile, GeoJSON, systèmes de coordonnées, carte choroplèthe
- Streamlit : mise en page, filtres, indicateurs, mise en cache des données
- Conteneuriser son application : `Dockerfile`, `requirements.txt`, profil Docker Compose

## Démonstration

1. Notebook **`05a_plotly_altair.ipynb`** : graphiques interactifs, vues liées, conversion des contours en `data/zones.geojson`
2. Application **`app/app.py`** :

```bash
docker compose --profile app up -d --build
```

puis http://localhost:8501

## À vous de jouer

1. Faites les trois exercices de fin de notebook dans l'application (`app/app.py`).
2. Ajoutez **une vue de votre choix** qui aide le responsable d'exploitation à décider où envoyer ses chauffeurs,
   et justifiez le type de graphique choisi (S04).
3. Question de réflexion : *pourquoi l'application lit-elle les tables gold de PostgreSQL plutôt que les fichiers du data lake ?*

## C'est réussi quand…

- l'application tourne dans son conteneur sur http://localhost:8501 ;
- les filtres mettent à jour les indicateurs, les courbes et la carte ;
- la vue que vous avez ajoutée répond à une question métier explicite.

## Dépôt pour le dossier MSPR 4.1

Captures de l'application + justification de vos choix de visualisation + votre `app.py`.

## Nettoyage

```bash
docker compose --profile app stop
```

## Séance suivante

[S06 — Storytelling et conception de dashboard](../S06-storytelling/README.md)
