# S02 — Préparation à l'échelle avec Spark

## Objectif

Transformer la couche *bronze* en données fiables (*silver*) puis en tables prêtes pour la décision (*gold*),
et les exposer dans PostgreSQL pour les outils de visualisation.

## Prérequis

- [S01](../S01-architectures/README.md) terminée : `bronze/yellow_trips`, `bronze/zones`, `bronze/meteo` existent
- `docker compose up -d`

## Apports

- Pourquoi nettoyer **dans Spark** : le volume (des millions de lignes) et la traçabilité des règles.
- Une règle de nettoyage = un nom + une condition + un comptage. On doit pouvoir justifier chaque ligne retirée.
- *Silver* : une ligne par fait, typée, propre. *Gold* : une table par usage (une question métier = une table).
- Jointures avec des données externes (météo) : alignement des clés de temps et des fuseaux horaires.
- La couche de restitution (PostgreSQL) : pourquoi les outils de BI ne lisent pas directement le data lake.

## Démonstration

Notebook **`02_silver_gold.ipynb`** : règles de nettoyage comptées → *silver* → deux tables *gold* → PostgreSQL → premiers graphiques.

## À vous de jouer

1. Exécutez le notebook, puis proposez **une règle de nettoyage supplémentaire** et justifiez-la.
2. Créez la table *gold* « aéroports » demandée en fin de notebook.
3. Vérifiez dans PostgreSQL que vos tables sont bien là :
   ```bash
   docker exec -it postgres psql -U cours -d nyctaxi -c "\dt"
   ```
4. Question de réflexion : *une course de 0,1 mile à 80 $ : erreur à supprimer ou cas réel à garder ?*

## C'est réussi quand…

- la console RustFS montre `silver/` et `gold/` ;
- `SELECT * FROM gold_trajets_horaires LIMIT 10;` répond dans PostgreSQL ;
- chaque règle de nettoyage est justifiée et chiffrée.

## Dépôt pour le dossier MSPR 4.1

Tableau des règles de nettoyage (règle, justification, lignes retirées) + description des tables *gold*.

## Nettoyage

```bash
docker compose stop
```

## Séance suivante

[S03 — Sémantique et graphes](../S03-semantique/README.md)
