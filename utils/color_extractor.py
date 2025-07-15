# utils/color_extractor.py

from colorthief import ColorThief
from PIL import Image
import os

def extract_palette(image_paths, num_colors=5):
    """
    Extracts a color palette from the first image in the list.
    For demo: uses first image — you can enhance to use all images.
    """
    palette = []

    if len(image_paths) == 0:
        return palette

    first_image_path = image_paths[0]

    try:
        color_thief = ColorThief(first_image_path)
        palette = color_thief.get_palette(color_count=num_colors)
    except Exception as e:
        print(f"[WARN] Failed to extract palette from {first_image_path}: {e}")

    return palette
