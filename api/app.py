import logging
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
from io import BytesIO
import base64
import os

app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Charger le modèle pré-entraîné
model = tf.keras.models.load_model('model.keras')

# Palette de couleurs
palette = {
    0: [0, 0, 0],         
    1: [128, 64, 128],    
    2: [70, 70, 70],      
    3: [255, 255, 0],    
    4: [107, 142, 35],    
    5: [70, 130, 180],    
    6: [220, 20, 60],     
    7: [0, 0, 142]        
}

def colorize_mask(mask):
    color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    for label, color in palette.items():
        color_mask[mask == label] = color
    return color_mask

def preprocess_image(image, target_size):
    original_size = image.size
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array.astype('float32'), original_size

@app.route("/health")
def health_check():
    try:
        if model is None:
            raise ValueError("Model is not loaded")
        logging.info("Health check passed")
        return jsonify({"status": "Healthy"}), 200
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify({"status": "Unhealthy", "error": str(e)}), 500

@app.route('/segment', methods=['POST'])
def segment():
    try:
        logging.info("Segment endpoint hit")
        
        # Check if an image file was uploaded
        if 'file' not in request.files:
            logging.error("No file part in the request")
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            logging.error("No file selected for uploading")
            return jsonify({"error": "No file selected for uploading"}), 400
        
        # Read the image file
        logging.info("Reading the image file")
        image = Image.open(file).convert('RGB')
        logging.info("Image received and decoded")

        # Preprocess the image and get its original size
        image_array, original_size = preprocess_image(image, (256, 256))
        logging.info(f"Image preprocessed to size {original_size}")

        # Predict the mask
        pred_mask = model.predict(image_array)
        pred_mask = np.argmax(pred_mask, axis=-1)[0]
        logging.info("Mask prediction completed")

        # Resize the mask to the original size
        pred_mask_resized = Image.fromarray(pred_mask.astype(np.uint8)).resize(original_size, Image.NEAREST)
        logging.info("Mask resized to original image size")

        # Colorize the mask
        color_mask = colorize_mask(np.array(pred_mask_resized))
        logging.info("Mask colorization completed")

        # Convert the mask to base64 for the response
        color_mask_image = Image.fromarray(color_mask)
        buffered = BytesIO()
        color_mask_image.save(buffered, format="PNG")
        color_mask_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        logging.info("Mask converted to base64")

        response = {
            'mask': color_mask_base64
        }
        return jsonify(response)

    except Exception as e:
        logging.error(f"Error during segmentation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
