import os
import base64
import requests
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from colorthief import ColorThief

from mood_lifting_map import mood_lifting_map

# Flask setup: Serve frontend from build folder
app = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(app)

# Leonardo AI Config
LEONARDO_API_KEY = "36176ce3-1981-4c04-89c7-61ad5b00f318"
LEONARDO_API_URL = "https://cloud.leonardo.ai/api/rest/v1/generations"

PROMPT_TEMPLATE = (
    "{mood} mood board where it has several images describing the emotion in an aesthetically "
    "pleasing layout with elements and shapes, pinterest styled, images clearly representing the "
    "emotion immersing the viewers"
)

def make_prompt(mood):
    return PROMPT_TEMPLATE.format(mood=mood)

def img_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def extract_hex_palette(base64_img_data):
    try:
        img_data = base64.b64decode(base64_img_data)
        img_io = BytesIO(img_data)
        color_thief = ColorThief(img_io)
        palette_rgb = color_thief.get_palette(color_count=5)
        return ['#%02x%02x%02x' % rgb for rgb in palette_rgb]
    except Exception as e:
        print(f"[WARN] Failed to extract palette: {e}")
        return []

def fetch_leonardo_images(prompt, num_images=4):
    headers = {
        "Authorization": f"Bearer {LEONARDO_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "modelId": "e316348f-7773-490e-adcd-46757c738eb7",  # Phoenix 1.0
        "num_images": num_images,
        "width": 512,
        "height": 512,
        "promptMagic": True,
        "nsfw": False
    }

    start_response = requests.post(LEONARDO_API_URL, headers=headers, json=payload)
    if start_response.status_code != 200:
        print("Leonardo error:", start_response.text)
        raise Exception("Failed to start generation")

    generation_id = start_response.json().get("sdGenerationJob", {}).get("generationId")
    if not generation_id:
        raise Exception("No generationId returned")

    poll_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    images_b64 = []

    import time
    for _ in range(20):
        poll_response = requests.get(poll_url, headers=headers)
        if poll_response.status_code != 200:
            raise Exception("Polling failed")

        poll_data = poll_response.json()
        images = poll_data.get("generations_by_pk", {}).get("generated_images", [])

        if images:
            for img_info in images:
                img_url = img_info.get("url")
                if img_url:
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        img = Image.open(BytesIO(img_response.content)).convert("RGB")
                        images_b64.append("data:image/png;base64," + img_to_base64(img))
            break
        time.sleep(1)

    if not images_b64:
        raise Exception("No images returned after polling")

    return images_b64

@app.route("/generate", methods=["POST"])
def generate_moodboard():
    data = request.json
    text_input = data.get("text_input", "").strip()
    lifting_mode = data.get("lifting_mode", False)

    if text_input:
        mood_text = text_input.lower()
    else:
        return jsonify({"error": "No text input provided"}), 400

    if lifting_mode:
        for neg, pos in mood_lifting_map.items():
            if neg in mood_text.split():
                print(f"[Mood Lifting] {mood_text} → {pos}")
                mood_text = pos
                break

    prompt = make_prompt(mood_text)

    try:
        images_b64 = fetch_leonardo_images(prompt)
        img_base64_data = images_b64[0].split(",")[-1]
        palette = extract_hex_palette(img_base64_data)

        return jsonify({
            "mood": mood_text,
            "prompt": prompt,
            "images": images_b64,
            "palette": palette
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve static frontend files
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
