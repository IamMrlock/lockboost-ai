#!/usr/bin/env python3
import os
import json
import re
from dotenv import load_dotenv
from rich import print
from rich.console import Console
import openai

console = Console()
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise SystemExit("[red]ERROR[/red] Set OPENAI_API_KEY in your .env file")

openai.api_key = OPENAI_API_KEY

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

def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    # Change 'model' if you don't have access. e.g. "gpt-3.5-turbo"
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role":"user","content":prompt}],
        max_tokens=700,
        temperature=0.8,
    )
    return resp["choices"][0]["message"]["content"]

def parse_text_to_structured(text: str):
    """
    Very simple parser: splits by lines and identifies numbered blocks.
    This is intentionally minimal — improve parsing later for production.
    """
    ideas = []
    # split by pattern "1." "2." etc
    parts = re.split(r'\n\s*\d+\.\s*', "\n" + text)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # naive extraction
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        title = lines[0] if lines else ""
        hook = ""
        caption = ""
        hashtags = []
        fmt = ""
        # try to find hashtags and format
        for l in lines[1:]:
            if l.lower().startswith("hook") or l.lower().startswith("- hook"):
                hook = l.split(":",1)[-1].strip()
            elif l.lower().startswith("caption") or l.lower().startswith("- suggested caption"):
                caption = l.split(":",1)[-1].strip()
            elif "#" in l:
                hashtags = re.findall(r"#\w+", l)
            elif any(k in l.lower() for k in ["carousel","reel","short","thread","tutorial"]):
                fmt = l
            else:
                # fallback append to caption if short
                if len(caption) < 200:
                    caption += " " + l
        ideas.append({
            "title": title,
            "hook": hook,
            "caption": caption.strip(),
            "hashtags": hashtags,
            "format": fmt
        })
    return ideas

def generate_ideas(topic: str, platform: str="Instagram", audience: str="young gamers and creators", tone: str="energetic, concise", model: str = "gpt-4o-mini", as_json: bool=False):
    prompt = PROMPT_TEMPLATE.format(platform=platform, audience=audience, tone=tone, topic=topic)
    console.log("Calling OpenAI...")
    text = call_openai(prompt, model=model)
    console.print("[bold green]Raw AI output:[/]\n")
    console.print(text)
    if as_json:
        console.log("Parsing to structured JSON (basic parser).")
        ideas = parse_text_to_structured(text)
        return {"topic": topic, "platform": platform, "audience": audience, "ideas": ideas}
    return {"raw": text}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LockBoostAI - content idea generator (MVP)")
    parser.add_argument("--topic", required=True, help="Topic or keyword")
    parser.add_argument("--platform", default="Instagram", help="Platform (Instagram, LinkedIn, TikTok...)")
    parser.add_argument("--audience", default="young gamers and creators", help="Target audience")
    parser.add_argument("--tone", default="energetic, concise", help="Tone")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model to use")
    parser.add_argument("--json", action="store_true", help="Return simple structured JSON")
    args = parser.parse_args()

    out = generate_ideas(args.topic, args.platform, args.audience, args.tone, args.model, args.json)
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))