import requests
import json
import os
from openai import OpenAI
import base64
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join("backend", "outputs") 
def _save_b64_png(b64: str, prefix: str) -> str:
    fname = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
    fpath = os.path.join(SAVE_DIR, fname)
    with open(fpath, "wb") as f:
        f.write(base64.b64decode(b64))
    return fpath

def image_gen(json_path: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    print("API key loaded:", os.environ.get("OPENAI_API_KEY")[:7] + "...")
    print("If you see nothing you don't have the api key lol")

    with open(json_path, "r", encoding="utf-8") as f:
        j = json.load(f)

    if not os.path.exists(json_path):
        print("Can't find the file lol.")
        exit()

    prompt = (j.get("transcript") or "Not Found") 

    if prompt == "Not Found":
        print("lol didnt work")
        exit()
    else:
        print(f"Here is the prompt: {prompt}")
    print("Working on it.... wait some time")

    content = f"""
    Create a children's picture-book outline from this idea.
Age target: 5. Maximum pages: 4.

Return STRICT JSON with this schema:
{{
  "style": {{
    "art_style": "short phrase (e.g., soft watercolor, thick outlines)",
    "palette": "2–4 colors (e.g., soft pastels: peach, mint, sky blue)",
    "composition_rules": "short list (e.g., centered main character, simple backgrounds)"
  }},
  "characters": [
    {{
      "name": "Character's name",
      "visual": "distinctive visual description (colors, shapes, markings)",
      "personality": "few friendly traits"
    }}
  ],
  "pages": [
    {{
      "page_number": 1,
      "narration": "1–2 short sentences for kids",
      "illustration_prompt": "A FULLY SELF-CONTAINED prompt that restates the character and style without pronouns."
    }}
  ]
}}

Rules:
- Each page must be understandable in isolation.
- There should be no text in the images, do not generate text in the images.
- In 'illustration_prompt', restate the main character's name and defining visual traits every time.
- Do NOT embed text inside the image; narration is separate.
- Stay cheerful and safe.
Idea: {prompt}
    """
    SYSTEM = """You are a children's author & illustrator assistant.
Return STRICT JSON only (no prose). Keep language gentle and age-appropriate.
Never use pronouns like 'she/he/they' in illustration prompts; restate the character. Never use text within
the images. 
"""
    resp = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},   # forces valid JSON
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": content},
    ],
    )   
    outline = json.loads(resp.choices[0].message.content)
    style = outline.get("style") # getting style
    characters = outline.get("characters") # getting characters

    saves = []
    pages = outline.get("pages")
    print("Heres what chatgpt makes")
    print(resp.choices[0].message.content)
    for p in pages:
        page_no = p.get("page_number")
        illop = (p.get("illustration_prompt") or "").strip()
        if not illop:
            # fallback to narration if illustration prompt missing
            illop = (p.get("narration") or "").strip()
        if not illop:
            continue

        full_prompt = "illustration = " + illop + "narration = " + p.get("narration")
        gen = client.images.generate(
            model="gpt-image-1",
            prompt=full_prompt,
            size="1024x1024",
            quality="low"
        )
        path = _save_b64_png(gen.data[0].b64_json, f"page_{page_no:02d}")
        saves.append({
            "page_number": page_no,
            "path": path,
            "url": "/outputs/" + os.path.basename(path),
            "narration": p.get("narration") or ""
        })
        print(f"Page {page_no} is done. Moving on!")
    print("Done! bye.")
    print("Done! bye.")
    print("Done! bye.")
    print("Done! bye.")
    print("Heres the json btw")
    return saves


if __name__ == "__main__":
    print(image_gen(os.path.join(BASE_DIR, "transcript.json")))