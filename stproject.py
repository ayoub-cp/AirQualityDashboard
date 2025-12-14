import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO

# -----------------------------
# CONFIG PAGE
# -----------------------------
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("🌍 Air Quality Data Visualization")

# -----------------------------
# SESSION STATE
# -----------------------------
if "selected_graph" not in st.session_state:
    st.session_state["selected_graph"] = None

# -----------------------------
# LOAD & CLEAN DATA
# -----------------------------
@st.cache
def load_data(path):
    df = pd.read_csv(path, sep=";", decimal=",")
    df = df.dropna(axis=1, how="all")
    df.replace(-200, np.nan, inplace=True)
    df["Datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"], format="%d/%m/%Y %H.%M.%S", errors="coerce"
    )
    df.drop(columns=["Date", "Time"], inplace=True)
    numeric_cols = df.columns.drop("Datetime")
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df[numeric_cols] = df[numeric_cols].apply(lambda x: x.fillna(x.median()))
    df.sort_values("Datetime", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

df = load_data("C:/Users/ASUS/Desktop/py project/data/AirQualityUCI.csv")

# -----------------------------
# INTRODUCTION ET APERCU DES DONNEES
# -----------------------------
st.subheader("Introduction")
st.write("""
Bienvenue dans le tableau de bord de **qualité de l'air**.  
Ce projet analyse les concentrations de divers polluants mesurés à Milan, Italie.  
Vous pouvez explorer les données et visualiser les tendances grâce aux graphiques interactifs.
""")

st.subheader("Aperçu des données")
st.dataframe(df.head(5))
st.write("Statistiques descriptives :")
st.dataframe(df.describe())

# -----------------------------
# MENU EN HAUT AVEC ICONES
# -----------------------------
st.subheader("Sélectionnez un graphique")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📈 CO over time"):
        st.session_state["selected_graph"] = "CO(GT) over time"

with col2:
    if st.button("📊 NO2 distribution"):
        st.session_state["selected_graph"] = "NO2(GT) distribution"

with col3:
    if st.button("🌡️ Temp vs Humidity"):
        st.session_state["selected_graph"] = "Temperature vs Relative Humidity"

with col4:
    if st.button("🔵 CO & NO2 over time"):
        st.session_state["selected_graph"] = "CO and NO2 over time"

with col5:
    if st.button("📦 Pollutant boxplot"):
        st.session_state["selected_graph"] = "Pollutant boxplot"

# -----------------------------
# AFFICHER LE GRAPHIQUE
# -----------------------------
if st.session_state["selected_graph"] is not None:
    st.write("---")
    st.button("⬅️ Retour", on_click=lambda: st.session_state.update({"selected_graph": None}))

    fig, ax = plt.subplots(figsize=(12,5))

    if st.session_state["selected_graph"] == "CO(GT) over time":
        ax.plot(df["Datetime"], df["CO(GT)"], color='steelblue')
        ax.set_xlabel("Time")
        ax.set_ylabel("CO (mg/m³)")
        ax.set_title("Carbon Monoxide Concentration Over Time")

    elif st.session_state["selected_graph"] == "NO2(GT) distribution":
        ax.hist(df["NO2(GT)"], bins=30, color='orange', edgecolor='black')
        ax.set_xlabel("NO2 Concentration")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of NO2 Levels")

    elif st.session_state["selected_graph"] == "Temperature vs Relative Humidity":
        ax.scatter(df["T"], df["RH"], color='green', alpha=0.6)
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("Relative Humidity (%)")
        ax.set_title("Temperature vs Relative Humidity")

    elif st.session_state["selected_graph"] == "CO and NO2 over time":
        ax.plot(df["Datetime"], df["CO(GT)"], label="CO", color='blue')
        ax.plot(df["Datetime"], df["NO2(GT)"], label="NO2", color='red')
        ax.set_xlabel("Time")
        ax.set_ylabel("Concentration")
        ax.set_title("CO and NO2 Over Time")
        ax.legend()

    elif st.session_state["selected_graph"] == "Pollutant boxplot":
        ax.boxplot([df["CO(GT)"], df["NO2(GT)"], df["C6H6(GT)"]])
        ax.set_xticklabels(["CO", "NO2", "Benzene"])
        ax.set_title("Pollutant Distribution & Outliers")

    st.pyplot(fig)

    # -----------------------------
    # BOUTON TELECHARGER LE GRAPHIQUE
    # -----------------------------
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.download_button(
        label="Télécharger le graphique",
        data=buf,
        file_name=f"{st.session_state['selected_graph'].replace(' ','_')}.png",
        mime="image/png"
    )

# -----------------------------
# CONCLUSION
# -----------------------------
st.write("---")
st.subheader("Conclusion")
st.write("""
L'analyse de ce dataset sur la qualité de l'air à Milan montre les tendances des principaux polluants.  
Ce tableau de bord permet de visualiser facilement les variations dans le temps et d'identifier les pics de pollution.
""")

# -----------------------------
# CRÉDITS
# -----------------------------
st.markdown(
    """
    <style>
    .author-text {
        position: fixed;
        top: 50px;
        right: 30px;
        font-size: 20px;
        font-weight: bold;
        color: #2E86C1;  /* bleu élégant */
        background-color: rgba(255, 255, 255, 0.7);  /* fond légèrement transparent */
        padding: 10px 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        z-index: 100;
    }
    </style>
    <div class="author-text">
        Créé par : Ayoub Garali et Mehrez Khemir
    </div>
    """,
    unsafe_allow_html=True
)
