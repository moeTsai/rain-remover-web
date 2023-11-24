import requests

server_url = 'http://localhost:5000/process_image'

img_path = 'path/to/your/image.jpg'
img = open(img_path, 'rb')

files = {'image': img}
response = requests.post(server_url, files=files)

if response.status_code == 200:
    processed_img_data = response.json()['processed_image']
else:
    print('Error:', response.text)
