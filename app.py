from flask import Flask, request, render_template, redirect, url_for
import os
from deepface import DeepFace

# Inisialisasi Flask
app = Flask(__name__)

# Folder untuk menyimpan file upload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    # Simpan file yang diunggah
    user_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(user_image_path)
    
    # Path ke gambar referensi
    reference_image_path = "mbape.jpg"  # Ganti dengan gambar referensi Anda
    
    # Bandingkan gambar yang diupload dengan gambar referensi
    result = DeepFace.verify(user_image_path, reference_image_path)
    
    if result["verified"]:
        return "Wajah cocok!"
    else:
        return "Wajah tidak cocok!"

if __name__ == '__main__':
    app.run(debug=True)
