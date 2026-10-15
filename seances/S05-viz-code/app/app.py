"""
Application d'analyse NYC Taxi — S05.

Lancement :   docker compose --profile app up -d --build
Adresse :     http://localhost:8501
"""
import json
import os

import pandas as pd
import plotly.express as px
import sqlalchemy
import streamlit as st

st.set_page_config(page_title="NYC Taxi — analyse", layout="wide")

PG = (f"postgresql+psycopg2://{os.getenv('PG_USER', 'cours')}:{os.getenv('PG_PASSWORD', 'cours')}"
      f"@{os.getenv('PG_HOST', 'postgres')}:5432/{os.getenv('PG_DB', 'nyctaxi')}")
GEOJSON = os.getenv("ZONES_GEOJSON", "/data/zones.geojson")


# --- Données (mises en cache : lues une seule fois) ---------------------------
@st.cache_data(ttl=600)
def charger():
    moteur = sqlalchemy.create_engine(PG)
    horaires = pd.read_sql("SELECT * FROM gold_trajets_horaires", moteur)
    zones = pd.read_sql("SELECT * FROM gold_zones", moteur)
    horaires["heure"] = pd.to_datetime(horaires["heure_pickup"]).dt.hour
    horaires["jour"] = pd.to_datetime(horaires["heure_pickup"]).dt.date
    
    # AJOUT EXERCICE 1 : Calcul du jour de la semaine
    jours = {0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi", 4: "vendredi", 5: "samedi", 6: "dimanche"}
    horaires["nom_jour"] = pd.to_datetime(horaires["heure_pickup"]).dt.dayofweek.map(jours)
    
    return horaires, zones


@st.cache_data
def contours():
    if not os.path.exists(GEOJSON):
        return None
    with open(GEOJSON, encoding="utf-8") as f:
        return json.load(f)


horaires, zones = charger()
geo = contours()

# --- Filtres -------------------------------------------------------------------
st.sidebar.header("Filtres")
arrondissements = sorted(a for a in horaires["arrondissement"].dropna().unique() if a not in ("Unknown", "N/A"))
choix = st.sidebar.multiselect("Arrondissements", arrondissements, default=arrondissements)
plage = st.sidebar.slider("Heures de prise en charge", 0, 23, (0, 23))

# AJOUT EXERCICE 1 : Sélecteur des jours
liste_jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
choix_jours = st.sidebar.multiselect("Jours de la semaine", liste_jours, default=liste_jours)

# MODIFICATION EXERCICE 1 : On intègre choix_jours dans le filtre
h = horaires[
    horaires["arrondissement"].isin(choix) & 
    horaires["heure"].between(*plage) &
    horaires["nom_jour"].isin(choix_jours)
]
z = zones[zones["arrondissement"].isin(choix)]

# --- Indicateurs -----------------------------------------------------------------
st.title("Où et quand les taxis gagnent-ils le plus ?")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Courses", f"{int(h['courses'].sum()):,}".replace(",", " "))
k2.metric("Revenu total", f"{h['revenu'].sum() / 1e6:,.1f} M$")
k3.metric("Prix moyen", f"{(h['revenu'].sum() / max(h['courses'].sum(), 1)):.2f} $")
k4.metric("Pourboire moyen", f"{(h['pourboire_moyen'] * h['courses']).sum() / max(h['courses'].sum(), 1):.2f} $")

# --- Graphiques ----------------------------------------------------------------
g1, g2 = st.columns(2)

par_heure = h.groupby(["heure", "arrondissement"], as_index=False)["courses"].sum()
fig = px.line(par_heure, x="heure", y="courses", color="arrondissement", markers=True,
              labels={"heure": "Heure de prise en charge", "courses": "Courses (mois)"},
              title="Activité par heure")
g1.plotly_chart(fig, use_container_width=True)

top = z.nlargest(15, "courses").sort_values("courses")
fig = px.bar(top, x="courses", y="zone", color="arrondissement", orientation="h",
             labels={"courses": "Courses (mois)", "zone": ""}, title="Les 15 zones de départ les plus actives")
g2.plotly_chart(fig, use_container_width=True)

# --- EXERCICE 2 : Le pourboire moyen dépend-il de l'heure ? ---
st.markdown("---") # Petite ligne de séparation visuelle
st.subheader("Comportement des passagers")

# 1. Calcul rigoureux du pourboire moyen pondéré par heure
h_temp = h.copy()
h_temp["pourboire_total"] = h_temp["pourboire_moyen"] * h_temp["courses"]
pourboire_heure = h_temp.groupby("heure", as_index=False).agg(
    courses_tot=("courses", "sum"),
    pourboire_tot=("pourboire_total", "sum")
)
pourboire_heure["pourboire_moyen_reel"] = pourboire_heure["pourboire_tot"] / pourboire_heure["courses_tot"]

# 2. Création du graphique Plotly
fig_pourboire = px.line(
    pourboire_heure, 
    x="heure", 
    y="pourboire_moyen_reel", 
    markers=True,
    labels={"heure": "Heure de la journée", "pourboire_moyen_reel": "Pourboire moyen ($)"},
    title="Évolution du pourboire moyen selon l'heure",
    color_discrete_sequence=["#EF553B"] # Couleur différente pour varier
)
# Règle d'or de la Dataviz : on force l'axe Y à commencer à 0
fig_pourboire.update_yaxes(rangemode="tozero")

st.plotly_chart(fig_pourboire, use_container_width=True)
st.markdown("---")
# --------------------------------------------------------------
if geo is not None:
    # MODIFICATION EXERCICE 3 : color="courses" au lieu de "prix_moyen"
    fig = px.choropleth_map(z, geojson=geo, locations="PULocationID", featureidkey="properties.LocationID",
                            color="courses", hover_name="zone", 
                            hover_data={"courses": True, "prix_moyen": ":.2f", "PULocationID": False},
                            color_continuous_scale="Viridis", map_style="carto-positron",
                            center={"lat": 40.73, "lon": -73.94}, zoom=9.3, opacity=0.75,
                            labels={"courses": "Nombre de courses"}, title="Nombre de courses par zone de départ")
    fig.update_layout(height=600, margin={"l": 0, "r": 0, "t": 40, "b": 0})
    st.plotly_chart(fig, use_container_width=True)
    
    # REPONSE A LA QUESTION DE L'EXERCICE 3 (affichée directement sur la page)
    st.info("**Pourquoi faudrait-il utiliser une échelle logarithmique ?**\n"
            "Parce que les écarts de fréquentation sont immenses. Certaines zones de Manhattan comptabilisent "
            "plus de 100 000 courses, tandis que la banlieue n'en a que quelques dizaines. "
            "Avec cette échelle linéaire classique, Manhattan sature totalement la palette de couleurs, "
            "rendant le reste de la carte illisible (toutes les autres zones paraissent de la même couleur claire).")
else:
    st.info("Carte indisponible : lancez d'abord le notebook 05a pour créer data/zones.geojson.")

with st.expander("Voir les données"):
    st.dataframe(z.sort_values("courses", ascending=False), use_container_width=True)
    # --- VUE MÉTIER : Aide à la décision ---
st.markdown("---")
st.subheader("Aide à la décision : Où génère-t-on le plus de revenus ?")

# 1. Calcul du revenu total généré par chaque zone (Volume * Prix moyen)
z_metier = z.copy()
z_metier["revenu_total"] = z_metier["courses"] * z_metier["prix_moyen"]
top_revenus = z_metier.nlargest(10, "revenu_total").sort_values("revenu_total")

# 2. Création du graphique (Barres horizontales triées)
fig_metier = px.bar(
    top_revenus, 
    x="revenu_total", 
    y="zone", 
    color="arrondissement", 
    orientation="h",
    labels={"revenu_total": "Chiffre d'affaires total ($)", "zone": ""}, 
    title="Top 10 des zones générant le plus d'argent (Volume × Prix)"
)

st.plotly_chart(fig_metier, use_container_width=True)

# 3. Justification exigée par la consigne (affichée sur la page)
st.success(
    "**Justification du choix (S04) :** Pour aider le responsable à savoir *où* envoyer ses chauffeurs, "
    "j'ai calculé le revenu total (courses × prix). J'ai choisi un **diagramme en barres horizontales triées**, "
    "car c'est la représentation visuelle la plus efficace pour comparer des catégories (les zones) "
    "et identifier un classement au premier coup d'œil."
)
# --- QUESTION DE RÉFLEXION FINALE ---
st.markdown("---")
st.subheader("Question de réflexion : PostgreSQL vs Data Lake")
st.info(
    "**Pourquoi l'application lit-elle les tables gold de PostgreSQL plutôt que les fichiers du data lake ?**\n\n"
    "1. **Performance et Interactivité :** Une application web comme Streamlit exige des temps de réponse immédiats "
    "lorsqu'on utilise les filtres. PostgreSQL est un moteur optimisé avec des index pour requêter les données "
    "instantanément, contrairement à un Data Lake où la lecture de fichiers bruts (CSV, Parquet) serait beaucoup trop lente à chaque clic.\n\n"
    "2. **Qualité de la donnée (Couche Gold) :** Le Data Lake stocke souvent la donnée brute (Bronze). "
    "En lisant les tables 'gold' dans PostgreSQL, on s'assure de requêter une donnée déjà nettoyée, "
    "agrégée par la pipeline de données (Spark/Airflow), allégeant ainsi le travail de l'application."
)