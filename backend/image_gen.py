import requests
import json
import os
from openai import OpenAI
import base64
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

print("API key loaded:", os.environ.get("OPENAI_API_KEY")[:7] + "...")
print("If you see nothing you don't have the api key lol")

with open("transcript.json", "r", encoding="utf-8") as f:
    j = json.load(f)


prompt = (j.get("transcript") or "Not Found") 

if prompt == "Not Found":
    print("lol didnt work")
    exit()
else:
    print(f"Here is the prompt: {prompt}")

result = client.images.generate(
    model = "gpt-image-1",
    prompt = prompt,
    size = "1024x1024",
    quality = "medium"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

save_dir = "outputs"               
os.makedirs(save_dir, exist_ok=True)  # create if not exists
save_path = os.path.join(save_dir, "pic.png")
print("Working on it.... wait some time")
with open(save_path, "wb") as f:
    f.write(image_bytes)

print("Image saved to:", save_path)


