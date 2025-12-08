#!/usr/bin/env python3
import os
import json
import re
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from openai import OpenAI

# --- LOAD ENV ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("[red]ERROR[/red] Set OPENAI_API_KEY in your .env file")

# --- CLIENT ---
client = OpenAI(api_key=OPENAI_API_KEY)
console = Console()

# --- PROMPT TEMPLATE ---
PROMPT_TEMPLATE = """
You are an expert content strategist. Given a topic and a platform, generate 5 high-impact post ideas, each with:
- a short title (max 6 words)
- a 1-line hook
- a suggested caption/first paragraph (max 2 sentences)
- 3 hashtags
- suggested format (carousel, reel, short, thread, tutorial)

Make output clear and separate each idea with a numbered list.
Platform: {platform}
Audience: {audience}
Tone: {tone}
Topic: {topic}
"""

# --- FUNCTIONS ---
def call_openai(prompt: str, model: str = "gpt-4") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en création de contenu."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Erreur lors de l'appel à OpenAI : {e}"


def parse_text_to_structured(text: str):
    ideas = []
    parts = re.split(r'\n\s*\d+\.\s*', '\n' + text)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        title = lines[0] if lines else ""
        hook = caption = fmt = ""
        hashtags = []
        for l in lines[1:]:
            low = l.lower()
            if low.startswith("hook"):
                hook = l.split(":",1)[-1].strip()
            elif low.startswith("caption"):
                caption = l.split(":",1)[-1].strip()
            elif "#" in l:
                hashtags = re.findall(r"#\w+", l)
            elif any(k in low for k in ["carousel", "reel", "short", "thread", "tutorial"]):
                fmt = l.strip()
            else:
                if len(caption) < 200:
                    caption += " " + l
        ideas.append({
            "title": title,
            "hook": hook,
            "caption": caption.strip(),
            "hashtags": hashtags,
            "format": fmt,
        })
    return ideas


def generate_ideas(
    topic: str,
    platform: str = "Instagram",
    audience: str = "young gamers and creators",
    tone: str = "energetic, concise",
    model: str = "gpt-4",
    as_json: bool = False
):
    prompt = PROMPT_TEMPLATE.format(platform=platform, audience=audience, tone=tone, topic=topic)
    console.log("[cyan]Calling OpenAI...[/cyan]")
    text = call_openai(prompt, model=model)

    if not text:
        return {"error": "No response from OpenAI."}

    console.print("[bold green]Raw AI output:[/]")
    console.print(text)

    if as_json:
        console.log("[yellow]Parsing to structured JSON...[/yellow]")
        ideas = parse_text_to_structured(text)
        return {
            "topic": topic,
            "platform": platform,
            "audience": audience,
            "ideas": ideas
        }

    return {"raw": text}


# --- CLI ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LockBoostAI - content idea generator (MVP)")
    parser.add_argument("--topic", required=True, help="Topic or keyword")
    parser.add_argument("--platform", default="Instagram", help="Platform (Instagram, LinkedIn, TikTok...)")
    parser.add_argument("--audience", default="young gamers and creators", help="Target audience")
    parser.add_argument("--tone", default="energetic, concise", help="Tone")
    parser.add_argument("--model", default="gpt-4", help="OpenAI model to use")
    parser.add_argument("--json", action="store_true", help="Return structured JSON")
    args = parser.parse_args()

    output = generate_ideas(
        args.topic,
        args.platform,
        args.audience,
        args.tone,
        args.model,
        args.json
    )

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(output.get("raw", "No output generated."))