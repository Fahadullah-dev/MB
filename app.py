# ai_moodboard_app.py

# TASK: Refactor this AI MoodBoard Generator to use image generation instead of image retrieval.

# CURRENT STATE:
# - The system currently uses CLIP + FAISS to find similar face images based on mood input (text or image).
# - It retrieves existing images of faces from a dataset, not suitable for a moodboard.

# GOAL:
# - Replace the FAISS + face retrieval system with an AI image generation model like Stable Diffusion.
# - For a given mood input (e.g., "romantic", "calm", "anxious"):
#     → Generate 3-6 AI images matching that mood using Stable Diffusion.
#     → Extract a color palette from the generated images (keep existing function).
#     → Return the generated images and color palette as a moodboard.

# OPTIONAL:
# - Add a "Mood Lifting" feature that maps negative moods to positive ones before image generation.
# - Keep the existing FANE face-to-emotion detection for image input (you already have predict_mood_from_face).
# - Add prompts like "a cozy calm room, soft lighting, warm colors" based on mood.

# IMPLEMENTATION TIPS:
# - Use the diffusers library (HuggingFace) to run Stable Diffusion locally or via API.
# - Prompt examples: "romantic aesthetic moodboard, pink roses, candles, soft lighting"
# - Use a fixed pipeline: text → prompt → generate → extract_palette → return

# Begin updating the generate_moodboard() function now...


import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import numpy as np
from PIL import Image, ImageDraw
from io import BytesIO
import base64

from utils.color_extractor import extract_palette
from utils.layout_selector import select_layout
from mood_lifting_map import mood_lifting_map
from diffusers import StableDiffusionPipeline

# Setup Flask
app = Flask(__name__)
CORS(app)

# Device and pipeline
device = "cuda" if torch.cuda.is_available() else "cpu"
sd_pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16 if device=="cuda" else torch.float32
).to(device)

# Prompt template
PROMPT_TEMPLATE = "{mood} moodboard, aesthetic, high quality, no text, no watermark"
def make_prompt(mood):
    return PROMPT_TEMPLATE.format(mood=mood)

# Convert image to base64
def img_to_base64(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# Convert base64 to BytesIO
def base64_to_io(b64_str):
    return BytesIO(base64.b64decode(b64_str))

@app.route("/generate", methods=["POST"])
def generate_moodboard():
    data = request.json
    text_input = data.get("text_input", "").strip()
    image_input_b64 = data.get("image_input", None)
    lifting_mode = data.get("lifting_mode", False)

    # Get mood text
    if text_input:
        mood_text = text_input.lower()
    elif image_input_b64:
        image_bytes = base64.b64decode(image_input_b64)
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        mood_text = predict_mood_from_face(image)
    else:
        return jsonify({"error": "No input provided"}), 400

    # Mood lifting
    if lifting_mode:
        for neg, pos in mood_lifting_map.items():
            if neg in mood_text.split():
                mood_text = pos
                break

    prompt = make_prompt(mood_text)

    # Generate images
    images_b64 = []
    pil_images = []
    for _ in range(4):
        if device == "cuda":
            with torch.autocast("cuda"):
                img = sd_pipe(prompt, height=512, width=512, num_inference_steps=50, guidance_scale=10.0).images[0]
        else:
            img = sd_pipe(prompt, height=512, width=512, num_inference_steps=50, guidance_scale=10.0).images[0]
        pil_images.append(img)
        images_b64.append(img_to_base64(img))

    # Extract color palette
    palette = extract_palette([img_to_base64(img) for img in pil_images])
    
    return jsonify({
        "mood": mood_text,
        "prompt": prompt,
        "images": images_b64,
        "palette": palette
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import send_from_directory

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join("frontend", "build", path)):
        return send_from_directory(os.path.join("frontend", "build"), path)
    else:
        return send_from_directory(os.path.join("frontend", "build"), "index.html")
