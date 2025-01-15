from flask import Flask, request, render_template
import os
from deepface import DeepFace

# Inisialisasi Flask
app = Flask(__name__)

# Folder untuk menyimpan file upload
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

REFERENCE_FOLDER = os.path.join(app.root_path, 'static', 'reference_images')

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
    
    # Simpan file yang diunggah di dalam folder 'static/uploads'
    user_image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(user_image_path)
    
    # Membaca semua gambar dalam folder referensi
    reference_images = [os.path.join(REFERENCE_FOLDER, f) for f in os.listdir(REFERENCE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not reference_images:
        return "Tidak ada gambar referensi di folder ulama."
    
    highest_similarity = 0
    best_match = None
    
    # Bandingkan gambar yang diupload dengan setiap gambar referensi
    for ref_image in reference_images:
        try:
            # Ambil nama ulama dari nama file (tanpa ekstensi)
            ulama_name = os.path.splitext(os.path.basename(ref_image))[0]  # Nama file tanpa ekstensi
            
            # Verifikasi dengan DeepFace
            result = DeepFace.verify(user_image_path, ref_image)
            similarity = result.get("distance", 1.0)  # Jarak atau tingkat kemiripan
            similarity_percentage = (1 - similarity) * 100  # Konversi ke persentase
            
            if similarity_percentage > highest_similarity:
                highest_similarity = similarity_percentage
                best_match = {
                    "ulama_name": ulama_name,
                    "similarity_percentage": round(similarity_percentage, 2),
                    "ref_image": os.path.basename(ref_image)  # Menyimpan nama file gambar referensi
                }
        except Exception as e:
            continue

    # Format hasil
    if best_match:
        # Tetapkan ambang batas minimum (misalnya 60%) untuk hasil yang dianggap cocok
        MINIMUM_SIMILARITY = 60.0
        if best_match['similarity_percentage'] >= MINIMUM_SIMILARITY:
            # Jika cocok di atas ambang batas, tampilkan hasil
            return render_template('result.html', best_match=best_match, user_image=file.filename)
        else:
            # Tetap kirimkan hasil dengan pesan bahwa kemiripan tertinggi tidak memenuhi ambang batas
            return render_template('result.html', best_match=best_match, user_image=file.filename, message=f"Kemiripan tertinggi adalah {best_match['similarity_percentage']}% dengan gambar {best_match['ulama_name']}.")
    else:
        return "Tidak ada gambar yang cocok ditemukan."

if __name__ == '__main__':
    app.run(debug=True)
