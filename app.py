import asyncio
from flask import Flask, request, render_template
from PIL import Image
import numpy as np
from clip import get_probs
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore_form')
def explore_form():
    return render_template('form.html')

def generate_categories(pests):
    return [f"a photo of the pest {x}" for x in pests]

@app.route('/process_form', methods=['POST'])
def process_form():
    if 'image' in request.files:
        file = request.files['image']
        if not file or file.filename == "":
            KeyError("No image uploaded!")

        image = Image.open(file.stream)
        image.save("./img/img_1.png")


        # categories
        with open("pests.json","r") as file:
            pests = json.load(file)


        dict_probs = get_probs(categories=generate_categories(pests))
        # Sorting the dictionary by key values
        sorted_dict_probs = dict(sorted(dict_probs.items(), key=lambda item: item[1]))

        # Printing the sorted dictionary

        output = ""
        for key, value in sorted_dict_probs.items():
            print((f"{key}: {value}"))
            output += (f"{key}: {value}")


    return render_template('identification.html', dict_probs=output)

if __name__ == '__main__':
    app.run(debug=True)
