from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel
import numpy as np

def get_probs(categories=None, is_url=False):
    # Load CLIP model and processor
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

    path = "./img/img_1.png"  # path to the image saved in app.py

    if is_url:
        # If the image is provided as a URL
        image = Image.open(requests.get(path, stream=True).raw)
    else:
        # If the image is a local file
        image = Image.open(path)

    # Preprocess inputs using CLIP processor
    if categories is None: categories = ["a photo of a corn rootworm", "a photo of a dog"]
    inputs = processor(text=categories, images=image, return_tensors="pt", padding=True)

    # Get model outputs
    outputs = model(**inputs)
    
    # Extract logits per image (image-text similarity scores)
    logits_per_image = outputs.logits_per_image
    
    # Apply softmax to get label probabilities
    probs = logits_per_image.softmax(dim=1)
    np_probs = probs.cpu().detach().numpy()[0]

    np.set_printoptions(formatter={'float': '{:.6f}'.format})

    return dict(zip(categories, np_probs))

