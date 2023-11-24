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
    image = img_array
    image = Image.fromarray(image)
    image.save("../backend/temp-Image/input.png")

    subprocess.call(["python", "../backend/test.py", "-opt=../backend/options/test/ir-sde.yml"])

    
    output_image_path = "../backend\outputs\model_output.png"
    processed_img = Image.open(output_image_path)


    return image, processed_img

@app.route('/')
def index():
    return render_template('index.html', processed_image_data=None)
"""
    

@app.route('/process_image', methods=['POST'])
def process_image_route():
    try:
        print('Received POST request')
        file = request.files['image']
        img = Image.open(file)

        processed_img = process_image(img)


        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()

        original_img_b64 = base64.b64encode(img.tobytes()).decode('utf-8')


        img_byte_array = io.BytesIO()
        processed_img.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()

        # Encode images to base64 for HTML display
        processed_img_b64 = base64.b64encode(processed_img.tobytes()).decode('utf-8')

        return render_template('index.html', original_image_data=original_img_b64, processed_image_data=processed_img_b64)
    except Exception as e:
        return jsonify({'error': str(e)})
    
"""

@app.route('/process_image', methods=['POST'])
def process_image_route():
    try:
        print('Received POST request')  # Added print statement
        file = request.files['image']
        img = Image.open(file)

        image, processed_img = process_image(img)

        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array = img_byte_array.getvalue()

        processed_img_byte_array = io.BytesIO()
        processed_img.save(processed_img_byte_array, format='PNG')
        processed_img_byte_array = processed_img_byte_array.getvalue()
        # print(type(img_byte_array))

        # Encode processed image data to base64 for displaying in HTML
        processed_image_data = base64.b64encode(processed_img_byte_array).decode('utf-8')
        original_image_data = base64.b64encode(img_byte_array).decode('utf-8')

        return render_template('index.html', original_image_data=original_image_data, processed_image_data=processed_image_data)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
