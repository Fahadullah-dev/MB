# utils/layout_selector.py

def select_layout(mood_text):
    """
    Dummy layout selector — in real app, you can define many templates.
    Here we return just image paths as 'layout'.
    """
    # For demo — just return 'grid' layout style based on mood
    if mood_text in ["happy", "joyful", "inspired"]:
        layout = "bright_grid"
    elif mood_text in ["sad", "calm", "relaxed"]:
        layout = "soft_grid"
    elif mood_text in ["angry", "fear", "confused"]:
        layout = "balanced_grid"
    else:
        layout = "default_grid"

    return layout
