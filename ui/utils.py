import os
import re
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

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


def call_openai(prompt: str, model: str = "gpt-4o-mini"):
    """Basic OpenAI chat call."""
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.8,
    )
    return response["choices"][0]["message"]["content"]


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


def generate(topic, platform, audience, tone, model):
    prompt = PROMPT_TEMPLATE.format(
        platform=platform,
        audience=audience,
        tone=tone,
        topic=topic,
    )
    raw_output = call_openai(prompt, model=model)
    return parse_to_dict(raw_output)