# 🔒 LockBoostAI

**LockBoostAI** — Lightweight content idea generator for creators, marketers, and gaming communities.  
Generate high-impact post ideas, hooks, and short captions tailored to platforms (Instagram, TikTok, LinkedIn, etc.) quickly and easily.

---

## 🚀 MVP Overview

LockBoostAI provides a minimal but fully usable content booster for creators:

- Input a **topic**, **audience**, and **platform**.
- Get **5 curated post ideas** with titles, hooks, captions, and hashtags.
- Designed for **rapid iteration** and **real-world use** by creators, social media managers, and marketers.

Built for: **Mr Lock — gaming, marketing & NFT audience**.

---

## ⚙️ Quickstart

Follow these steps to run the project locally:

1. **Clone the repo**
```bash
git clone git@github.com:YOUR_USERNAME/lockboost-ai.git
cd lockboost-ai
```
## Create a virtual environment and activate it
```bash
python -m venv .venv
source .venv/bin/activate
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run the Streamlit app
```bash
streamlit  run app.py
```

## Automation script
I create for you a script that can help you running the app more quickly
#!/bin/bash
# --- Virtual env activation ---
source ui/.venv/bin/activate

# --- Installe les packages manquants ---
pip install --upgrade pip
pip install -r ui/requirements.txt 2>/dev/null || pip install streamlit openai python-dotenv

# --- Lance l'app ---
streamlit run ui/app.py


## 📝 How to Use lockboost ai
Enter a topic or prompt.
Select the audience (e.g., professionals, students, general public).
Choose a tone (friendly, formal, persuasive, humorous).
Select the platform (Instagram, TikTok, LinkedIn, etc.).
Click Generate to receive 5 curated content ideas.

## 🤝 Contributing
*We welcome contributions ! Follow these steps to add your work*
1. *Fork the repository on github*
2. *Clone your fork locally :* 
```bash
git clone git@github.com:YOUR_USERNAME/lockboost-ai.git
cd lockboost-ai
```
3. *Create a new branch for your feature/fix*
```bash
git checkout -b feature/my-new-feature
```
4. *Make your change and commit :*
```bash
git add .
git commit -m "Add description of your feature"
```
5. *Push your branch to your fork :*
```bash
git push origin feature/my-new-feature
```

## Open a pull request to the main repository's
Keep each branch focused on a single feature or bug fix


## 📄 PROJECT STRUCTURE
```graphql
lockboost-ai/
├─ app.py             # Main Streamlit app
├─ utils.py           # Helper functions (prompt generation, formatting)
├─ requirements.txt   # Python dependencies
├─ README.md          # Project info and instructions
└─ .gitignore         # Ignore venv, cache files, etc.
```

## 💡 Tips
Test your changes locally before opening a PR.
Resolve conflicts before pushing if you updated from upstream.
Keep PRs small and focused.
Engage in code review discussions to maintain quality.


## 🔗 USEFUL LINK
GitHub Issues: [link-to-issues]
Discussions: [link-to-discussions]
Streamlit Documentation: https://docs.streamlit.io

## 📜 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
