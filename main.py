###------------------ IMPORTS ------------------###
from flask import Flask, render_template_string, send_from_directory, request, redirect, url_for
import webbrowser
import os
import requests
import json

###------------------ SETUP ------------------ ###

"""
VARIABLES
CODY WASHINGTON
"""
WebApplication: Flask = Flask(__name__, static_folder = 'src')
ExcludedImages = ['AddImageIcon.png']
JSONFilePath = os.path.join('src', 'moodboard.json')

"""
Index.HTML Content JS, CSS, HTML
@saahir.lol
"""
HTML_Content = """
<!DOCTYPE html>
    <html>
    <head>
        <title>Moodboard</title>
        <style>
            html, body {
                background-color: black;
                margin: 0;
                padding: 0;
                height: 100%;
            }
            .top-bar {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: linear-gradient(to bottom, rgba(51, 51, 51, 0.5), rgba(0, 0, 0, 0.8));
                color: white;
                text-align: center;
                padding: 10px 0;
                z-index: 1000;
                display: flex;
                align-items: center;
            }
            .top-bar img {
                cursor: pointer;
            }
            .add-button {
                margin-left: 10px; 
                margin-right: 10px;
            }
            .add-button-container {
                display: flex;
                align-items: center;
            }
            .image-container {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 10px;
                margin-top: 100px;
                padding: 0;
            }
            .image-container img {
                width: 100%;
                height: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="top-bar">
                <span style="flex: 1;">IMAGE BOARD</span>
                <div class="add-button-container">
                    <img src="src\AddImageIcon.png" alt="Add Image" width="20" class="add-button" id="add-button">
                </div>
            </div>
            <div class="image-container" id="image-container">
                <form action="{{ url_for('add_image') }}" method="POST" enctype="multipart/form-data">
                    <input type="file" id="file-upload" name="file" style="display: none;">
                    <input type="submit" style="display: none;"> <!-- Hidden submit button to trigger file upload -->
                </form>
            </div>
        </div>
        <script>
            document.getElementById('add-button').addEventListener('click', function() {
                document.getElementById('file-upload').click();
            });
            document.getElementById('file-upload').addEventListener('change', function() {
                var fileInput = this;
                var file = fileInput.files[0];
                if (file) {
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        var img = document.createElement('img');
                        img.src = e.target.result;
                        img.onclick = function() {
                            removeImage(img);
                        };
                        var container = document.getElementById('image-container');
                        container.appendChild(img);
                        // Save the image data to the JSON file
                        saveImage(e.target.result);
                    };
                    reader.readAsDataURL(file);
                }
            });
            
            var savedImages = localStorage.getItem('moodboard');
            if (savedImages) {
                savedImages = JSON.parse(savedImages);
                var container = document.getElementById('image-container');
                savedImages.forEach(function(imageData) {
                    var img = document.createElement('img');
                    img.src = imageData;
                    img.onclick = function() {
                        removeImage(img);
                    };
                    container.appendChild(img);
                });
            }
            
            var savedImages = localStorage.getItem('moodboard');
            if (savedImages) {
                savedImages = JSON.parse(savedImages);
                var container = document.getElementById('image-container');
                savedImages.forEach(function(imageData) {
                    var img = document.createElement('img');
                    img.src = imageData;
                    container.appendChild(img);
                });
            }
            
            function removeImage(img) {
                var container = document.getElementById('image-container');
                container.removeChild(img);
                // Remove the image data from local storage
                var savedImages = localStorage.getItem('moodboard');
                if (savedImages) {
                    savedImages = JSON.parse(savedImages);
                    var index = savedImages.indexOf(img.src);
                    if (index !== -1) {
                        savedImages.splice(index, 1);
                        localStorage.setItem('moodboard', JSON.stringify(savedImages));
                    }
                }
            }
        </script>
    </body>
</html>
"""

###------------------ DEFINE ------------------###
"""
Save the image data to the JSON file
Cyncere Lindsey
"""
def load_images_from_json():
    saved_images = []
    if os.path.exists(JSONFilePath):
        with open(JSONFilePath, 'r') as json_file:
            saved_images = json.load(json_file)
    return saved_images

"""
Fetches random images from the Unsplash API
Cody Washington
"""
@WebApplication.route('/fetch_random_images')
def fetchRandomImages(count = 10):
    #Good use of APIs
    access_key = 'x-m8dd3nwb6kpZzYWwkEYvlUTNXO4IBHBeLOTqiAoxQ' # <------ Replace with your own access key (END-USER)
    base_url = 'https://api.unsplash.com/photos/random'
    RandomImages = []
    #Good use of for loop
    for Image in range(count):
        params = {
            'count': 1,
            'client_id': access_key,
        }
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            RandomImage = response.json()[0]
            RandomImageURL = RandomImage['urls']['regular']
            RandomImages.append(RandomImageURL)
    return RandomImages

"""
Save the image data a JSON file
Cody Washington
"""
@WebApplication.route('/save_image', methods=['POST'])
def save_image():
    data = request.json
    #Good logged error checking
    if "image" in data:
        saved_images.append(data["image"])
        return jsonify({"message": "Image saved successfully"})
    return jsonify({"message": "Image not saved"})

"""
Index page
Cody Washington
"""
@WebApplication.route('/')
def index() -> None:
    #Good use of embedded for loop
    image_files = [f for f in os.listdir('src') if f.endswith(('.png', '.jpg', '.jpeg', '.gif')) and f not in ExcludedImages]
    random_image_urls = fetchRandomImages(5)
    return render_template_string(HTML_Content, images = image_files, random_image_urls = random_image_urls)

"""
Sends new images to the page from the src folder
Cyncere Lindsey
"""
@WebApplication.route('/src/<filename>')
def send_image(filename):
    return send_from_directory('src', filename)

"""
Adds new images to the webpage
Cyncere Lindsey
"""
@WebApplication.route('/add_image', methods=['POST'])
def add_image() -> redirect:
    #Good use of if statement to check for cases
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        if uploaded_file.filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            uploaded_file.save(os.path.join('src', uploaded_file.filename))
    return redirect(url_for('index'))

###------------------ RUN CODE ------------------###
if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    WebApplication.run(debug=True)