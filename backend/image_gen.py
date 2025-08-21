import requests
import json
import os
from openai import OpenAI
import base64
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    result = client.images.generate(
        model = "gpt-image-1",
        prompt = prompt,
        size = "1024x1024",
        quality = "low"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    save_dir = os.path.join("backend", "outputs")           
    filename = f"pic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"    
    os.makedirs(save_dir, exist_ok=True)  # create if not exists
    save_path = os.path.join(save_dir, filename)
    with open(save_path, "wb") as f:
        f.write(image_bytes)

    print("Image saved to:", save_path)
    return save_path


if __name__ == "__main__":
    print(image_gen(os.path.join(BASE_DIR, "transcript.json")))