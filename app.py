from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore_form')
def explore_form():
    return render_template('form.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            # Convert the Image file to a numpy array
            image = Image.open(file.stream)
            image_np = np.array(image)
            print(f"Image converted to numpy array: \n{image_np}")
        else:
            print("No image uploaded")

    crop_name = request.form.get('crop_name')
    print(f"Crop Name: {crop_name}")

    # Redirect or respond here after processing
    return "Form submitted and processed"

if __name__ == '__main__':
    app.run(debug=True)
