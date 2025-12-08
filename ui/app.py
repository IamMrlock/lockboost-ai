import streamlit as st
from utils import generate

# --- CONFIG GLOBALE ---
st.set_page_config(
    page_title="LockBoost AI",
    page_icon="⚡",
    layout="wide"
)

# --- CSS CUSTOM ULTRA STYLÉ ---
st.markdown("""
<style>

body {
    background-color: #070B18;
    color: #E5E7EB;
}

/* Fade-in global */
.main {
    animation: fadeIn 0.8s ease-in-out;
}

/* Title neon */
.neon-title {
    font-size: 3rem;
    font-weight: 800;
    color: #fff;
    text-shadow: 0 0 12px #6366F1, 0 0 22px #14B8A6;
    animation: pulseGlow 3s infinite;
}

/* Subheader */
.sub-text {
    color: #9CA3AF;
    font-size: 1.2rem;
    margin-top: -10px;
    margin-bottom: 20px;
}

/* Inputs */
.stTextArea textarea {
    background-color: #111827 !important;
    color: #E5E7EB !important;
    border-radius: 12px !important;
    border: 1px solid #1F2937 !important;
    animation: fadeIn 1s;
}

/* Generer button */
.stButton>button {
    background: linear-gradient(135deg, #6366F1, #14B8A6);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1.5rem;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 0 10px rgba(99,102,241,0.4);
    transition: 0.25s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(20,184,166,0.6);
}

/* Result container */
.result-box {
    background-color: #0D1224;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #1F2937;
    margin-top: 20px;
    animation: fadeInUp 0.6s ease-out;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0A0F1F;
}
.sidebar-title {
    font-size: 1.5rem;
    color: #fff;
    font-weight: 700;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0% { text-shadow: 0 0 12px #6366F1; }
    50% { text-shadow: 0 0 25px #14B8A6; }
    100% { text-shadow: 0 0 12px #6366F1; }
}

</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("<div class='sidebar-title'>🧠 LockBoost AI</div>", unsafe_allow_html=True)
st.sidebar.write("Ton assistant créatif nouvelle génération.")
st.sidebar.markdown("---")

model = st.sidebar.selectbox(
    "🤖 Modèle IA",
    ["gpt-4.1-mini", "gpt-4.1", "gpt-5.1-mini", "gpt-5.1"],
)

st.sidebar.markdown("### 🗂️ Historique")
if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    st.sidebar.write(f"- {msg[:30]}...")

st.sidebar.markdown("---")
st.sidebar.caption("MVP v1.1 • by Lock")

# --- HEADER ---
st.markdown("<h1 class='neon-title'>⚡ LockBoost AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Le générateur d'idées qui upgrade ton contenu en 5 secondes.</p>", unsafe_allow_html=True)

# --- INPUT ---
prompt = st.text_area(
    "💬 Décris ce dont tu as besoin",
    placeholder="Ex : Donne-moi 5 idées de posts Instagram pour une marque beauté...",
    height=160
)

# --- ACTION BUTTON ---
generate_btn = st.button("⚡ Générer maintenant")

# --- LOGIC ---
if generate_btn:
    if prompt.strip() == "":
        st.warning("⚠️ Entre un prompt valide bro.")
    else:
        with st.spinner("⚡ Création en cours..."):
            response = generate(prompt, model)

        st.session_state.history.append(prompt)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### 🚀 Résultat")
        st.write(response)
        st.markdown("</div>", unsafe_allow_html=True)

        st.code(response, language="markdown")