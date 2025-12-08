import streamlit as st
from utils import generate  # remplace par le bon module si nécessaire

st.title("LockBoost AI 🚀")

# Inputs utilisateur
prompt = st.text_area("Entre ton prompt ici :", "")
platform = st.selectbox("Choisis la plateforme :", ["Instagram", "TikTok", "LinkedIn", "Twitter"])
tone = st.selectbox("Choisis le ton :", ["Amical", "Professionnel", "Humoristique", "Persuasif"])
model = st.selectbox("Choisis le modèle :", ["gpt-4", "gpt-4-mini", "gpt-3.5-turbo"])

# Bouton pour générer
if st.button("Générer"):
    if not prompt.strip():
        st.warning("⚠️ Merci de renseigner un prompt avant de générer.")
    else:
        try:
            # Appel de la fonction generate avec le bon nom de paramètre
            result = generate(
                text=prompt,           # ici on map le prompt à text
                platform=platform,
                audience="Tout public",
                tone=tone,
                model=model
            )
            st.success("✅ Contenu généré avec succès !")
            st.text_area("Résultat :", result, height=300)
        except Exception as e:
            st.error(f"❌ Une erreur est survenue : {e}")