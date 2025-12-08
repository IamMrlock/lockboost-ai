#!/usr/bin/env python3
# migrate_openai_safe.py
import os, re, shutil, zipfile, sys

PROJECT_DIR = "."  # lance depuis la racine du repo

pattern1 = re.compile(r'openai\.ChatCompletion\.create\(')
pattern2 = re.compile(r'openai\.ChatCompletion\b')

new_call_openai_lines = [
"def call_openai(prompt: str, model: str = \"gpt-4\") -> str:",
"    import openai",
"    try:",
"        response = openai.chat.completions.create(",
"            model=model,",
"            messages=[",
"                {\"role\": \"system\", \"content\": \"Tu es un assistant expert en création de contenu.\"},",
"                {\"role\": \"user\", \"content\": prompt}",
"            ],",
"            temperature=0.7,",
"            max_tokens=800",
"        )",
"        return response.choices[0].message.content.strip()",
"    except Exception as e:",
"        return f\"Erreur lors de l'appel à OpenAI : {e}\"",
""
]

migrated = []
replaced_call = []
backups = []

def migrate_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    orig = content

    content = pattern1.sub("openai.chat.completions.create(", content)
    content = pattern2.sub("openai.chat.completions", content)

    if "def call_openai" in content:
        lines = content.splitlines()
        new_lines = []
        i = 0
        changed = False
        while i < len(lines):
            line = lines[i]
            if line.lstrip().startswith("def call_openai"):
                # insert new function (top-level assumed)
                for nl in new_call_openai_lines:
                    new_lines.append(nl)
                # skip original function block until next top-level def or EOF
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    if re.match(r'^\s*def\s+\w+\s*\(', nxt) and (len(nxt) - len(nxt.lstrip()) == 0):
                        break
                    i += 1
                changed = True
                continue
            else:
                new_lines.append(line)
                i += 1
        if changed:
            content = "\n".join(new_lines) + ("\n" if orig.endswith("\n") else "")
            replaced_call.append(path)

    if content != orig:
        backup = path + ".bak"
        shutil.copy2(path, backup)
        backups.append(backup)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        migrated.append(path)

def walk_and_migrate(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # skip virtual env folders commonly named venv, .venv, env
        dirs[:] = [d for d in dirs if d not in ("venv", ".venv", "env", "__pycache__")]
        for fname in files:
            if fname.endswith(".py"):
                migrate_file(os.path.join(root, fname))

if __name__ == "__main__":
    print("Lancement de la migration — sauvegardes .bak créées pour chaque fichier modifié.")
    walk_and_migrate(PROJECT_DIR)
    print(f"Fichiers migrés : {len(migrated)}")
    if migrated:
        for p in migrated:
            print(" -", p)
    if replaced_call:
        print("\nDéfinitions call_openai remplacées dans :")
        for p in replaced_call:
            print(" -", p)
    if backups:
        print(f"\nBackups créés : {len(backups)} (.bak)")
    print("\nVérifie ton projet, fais un `pip install -r requirements.txt` puis teste ton app.")