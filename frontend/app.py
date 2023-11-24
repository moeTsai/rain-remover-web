from flask import Flask, request, render_template, jsonify
from PIL import Image
import numpy as np
import io
import base64
import subprocess


app = Flask(__name__)

def process_image(img):
    # Image processing
    img_array = np.array(img)
    processed_img_array = img_array
    processed_img = Image.fromarray(processed_img_array)
    processed_img.save("../backend/temp-Image/input.png")
    subprocess.call(["python", "../backend/test.py", "-opt=../backend/options/test/ir-sde.yml"])
    return processed_img

@app.route('/')
def index():
    return render_template('index.html', processed_image_data=None)

@app.route('/process_image', methods=['POST'])
def process_image_route():
    try:
        print('Received POST request')  # Added print statement
        file = request.files['image']
        img = Image.open(file)

        processed_img = process_image(img)

        img_byte_array = io.BytesIO()
        processed_img.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()

        # Encode processed image data to base64 for displaying in HTML
        processed_image_data = base64.b64encode(img_byte_array).decode('utf-8')

        return render_template('index.html', processed_image_data=processed_image_data)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
