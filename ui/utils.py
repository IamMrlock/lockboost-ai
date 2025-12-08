import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT_TEMPLATE = """
You are an expert content strategist. Given a topic and a platform, generate 5 high-impact post ideas, each with:
- a title (max 6 words)
- a 1-line hook
- a caption (max 2 sentences)
- 3 hashtags
- suggested format (carousel, reel, short, thread, tutorial)

Platform: {platform}
Audience: {audience}
Tone: {tone}
Topic: {topic}

Return output as a numbered list (1. 2. 3. ...).
"""

def call_openai(prompt: str, model: str = "gpt-4") -> str:
    import openai
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en création de contenu."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erreur lors de l'appel à OpenAI : {e}"

def parse_to_dict(text: str):
    """Simple text parser to convert raw output into a list of idea dicts."""
    ideas = []
    parts = re.split(r"\n\s*\d+\.\s*", "\n" + text)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        lines = part.split("\n")
        title = lines[0]

        hook = ""
        caption = ""
        hashtags = []
        fmt = ""

        for line in lines[1:]:
            l = line.lower()

            if "hook" in l:
                hook = line.split(":", 1)[1].strip()
            elif "caption" in l:
                caption = line.split(":", 1)[1].strip()
            elif "#" in line:
                hashtags = re.findall(r"#\w+", line)
            elif any(f in l for f in ["carousel", "reel", "short", "thread", "tutorial"]):
                fmt = line.strip()

        ideas.append({
            "title": title,
            "hook": hook,
            "caption": caption,
            "hashtags": hashtags,
            "format": fmt
        })

    return ideas


# generate (post social media optimisé)
def generate(topic: str, platform: str, audience: str, tone: str, model: str = "gpt-4") -> str:
    prompt = f"""
    Tu es un expert en marketing digital et copywriting spécialisé dans les contenus viraux.

    Crée un post engageant pour {platform} destiné à {audience}.
    Ton : {tone}
    Sujet : {topic}

    Instructions :
    - Texte captivant et facile à lire
    - Hook initial ou question pour inciter à l’interaction
    - 3-5 phrases pour Instagram/TikTok, 4-7 phrases pour LinkedIn
    - Authentique, pas de jargon inutile

    Format attendu :
    Texte final prêt à poster
    """
    return call_openai(prompt, model=model)