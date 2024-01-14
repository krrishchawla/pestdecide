import asyncio
from flask import Flask, request, render_template
from PIL import Image
import numpy as np
from clip import get_probs
import json
from util import final_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore_form')
def explore_form():
    return render_template('form.html')

def generate_categories(pests):
    return [f"a photo of the pest {x}" for x in pests]

# @app.route('/process_form', methods=['POST'])
# def process_form():
#     if 'image' in request.files:
#         file = request.files['image']
#         if not file or file.filename == "":
#             KeyError("No image uploaded!")

#         image = Image.open(file.stream)
#         image.save("./img/img_1.png")


#         # categories
#         with open("pests.json","r") as file:
#             pests = json.load(file)


#         dict_probs = get_probs(categories=generate_categories(pests))
#         # Sorting the dictionary by key values
#         sorted_dict_probs = dict(sorted(dict_probs.items(), key=lambda item: item[1]))

#         # Printing the sorted dictionary

#         # output = ""
#         # for key, value in sorted_dict_probs.items():
#         #     print((f"{key}: {value}"))
#         #     output += (f"{key}: {value}")
#         pest, percentage = sorted_dict_probs.popitem()

#         crop = request.files['crop_name']
#         state = request.files['state']
#         answer = final_response(crop=crop, state=state, pest=pest, topk=3)

#         output = answer


#     return render_template('identification.html', dict_probs=output)

@app.route('/process_form', methods=['POST'])
def process_form():
    if 'image' not in request.files or request.files['image'].filename == "":
        return "No image uploaded!", 400  # Return an error message

    file = request.files['image']

    try:
        # Ensure the file is an image
        image = Image.open(file.stream)
        image.save("./img/img_1.png")
    except IOError:
        return "Invalid image file!", 400  # Return an error message

    # Retrieve text input from the form
    crop = request.form.get('crop_name', '')
    state = request.form.get('state', '')

    with open("pests.json", "r") as file:
        pests = json.load(file)

    dict_probs = get_probs(categories=generate_categories(pests))
    sorted_dict_probs = dict(sorted(dict_probs.items(), key=lambda item: item[1]))

    # Assuming you want the last item after sorting
    if sorted_dict_probs:
        pest, percentage = list(sorted_dict_probs.items())[-1]
        pest = pest.replace("a photo of the pest ", "")
        answer = final_response(crop=crop, state=state, pest=pest, topk=3)
        output = answer

        # Ensure output is a dictionary
        if isinstance(output, str):
            output = json.loads(output)

    else:
        output = "No pest data found"

    return render_template('identification.html', dict_probs=output, pest=pest, percentage=percentage, crop=crop, location=state)

if __name__ == '__main__':
    app.run(debug=True)
