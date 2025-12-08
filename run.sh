#!/bin/bash

# --- Active l'environnement virtuel ---
source ui/.venv/bin/activate

# --- Installe les packages manquants ---
pip install --upgrade pip
pip install -r ui/requirements.txt 2>/dev/null || pip install streamlit openai python-dotenv

# --- Lance l'app ---
streamlit run ui/app.py