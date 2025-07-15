# fane_loader.py

import os
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

# Define FANE emotion classes (based on your folder structure)
fane_classes = [
    "angry",
    "confused",
    "disgust",
    "fear",
    "happy",
    "neutral",
    "sad",
    "shy",
    "surprise"
]

# Load pre-trained model (we use simple ResNet18 here for FANE example)
# In full project you can use a better model (ResNet50, VGG16, etc.)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = models.resnet18(pretrained=True)
model.fc = torch.nn.Linear(model.fc.in_features, len(fane_classes))  # Adjust output layer
model = model.to(device)

# Load FANE-trained weights (you need to train this — OR I can give a pretrained example!)
# Example:
# model.load_state_dict(torch.load("fane_model.pth"))
# For now — we will skip and show template

model.eval()

# Image transforms (standard for FER)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# Predict mood from face image
def predict_mood_from_face(face_image):
    # Convert PIL Image
    image = transform(face_image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        _, predicted_idx = outputs.max(1)
        mood = fane_classes[predicted_idx.item()]
    return mood
