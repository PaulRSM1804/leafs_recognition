import os
from werkzeug.utils import secure_filename
import matplotlib
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from tensorflow import keras
import numpy as np
from keras.preprocessing import image
import matplotlib.pyplot as plt
import cv2

app = Flask(__name__)

# Configuración de la carpeta para subir imágenes y para almacenar imágenes espectrales
UPLOAD_FOLDER = 'uploads'
SPECTRAL_FOLDER = 'spectral'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SPECTRAL_FOLDER'] = SPECTRAL_FOLDER

# Cargar el modelo entrenado
model = keras.models.load_model('spectral_banana_detection_model.h5')

# Función para verificar la extensión del archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función para generar la imagen en formato espectral
def generate_spectral_image(filepath):
    # Aquí debes implementar el procesamiento de la imagen para convertirla en espectral
    # Esto puede implicar el uso de bibliotecas como OpenCV para aplicar transformaciones de imagen

    # Por ejemplo, puedes cargar la imagen original con OpenCV
    img = cv2.imread(filepath)

    # Luego, aplicar alguna transformación espectral (simulada)
    spectral_img = 255 - img  # Reemplaza esto con tu proceso de conversión

    # Guardar la imagen espectral en una ubicación específica
    spectral_filepath = os.path.join(app.config['SPECTRAL_FOLDER'], 'spectral_' + os.path.basename(filepath))
    cv2.imwrite(spectral_filepath, spectral_img)

    return spectral_filepath

@app.route('/')
def index():
    return render_template('index.html')


# Lista para almacenar las imágenes cargadas
uploaded_images = []

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_images.append(filepath)
    
    return render_template('result.html', uploaded_images=uploaded_images)

@app.route('/generate_spectral', methods=['POST'])
def generate_spectral():
    # Obtener la selección del usuario
    selected_image = request.form['spectral_image']
    
    # Procesar la imagen seleccionada y convertirla en espectral
    spectral_filepath = generate_spectral_image(selected_image)
    
    # Descargar la imagen espectral
    return send_from_directory(app.config['SPECTRAL_FOLDER'], os.path.basename(spectral_filepath))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/spectral/<filename>')
def spectral_file(filename):
    return send_from_directory(app.config['SPECTRAL_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port=8080)
