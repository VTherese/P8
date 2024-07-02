import streamlit as st
import requests
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# URL de l'API Flask
FLASK_API_URL = "http://app-segmentation.azurewebsites.net/segment"

st.set_page_config(page_title="Segmentation d'Images", page_icon="🚗")

def get_mask(image):
    try:
        logging.info("Sending image to segmentation API")
        buffered = BytesIO()
        image.save(buffered, format=image.format)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        response = requests.post(FLASK_API_URL, json={'image': img_str})
        logging.info(f"API response status code: {response.status_code}")
        
        if response.status_code == 200:
            mask_base64 = response.json()["mask"]
            mask_data = base64.b64decode(mask_base64)
            mask_image = Image.open(BytesIO(mask_data))
            return mask_image
        else:
            st.error("Erreur lors de la requête à l'API Flask")
            logging.error("Erreur lors de la requête à l'API Flask")
            return None
    except Exception as e:
        logging.error(f"Error during get_mask: {e}")
        st.error("Erreur lors de la requête à l'API Flask")
        return None

# Palette de couleurs
palette = {
    0: [0, 0, 0],         # void - noir
    1: [128, 64, 128],    # flat - mauve
    2: [70, 70, 70],      # construction - gris
    3: [255, 255, 0],     # object - jaune
    4: [107, 142, 35],    # nature - vert olive
    5: [70, 130, 180],    # sky - bleu
    6: [220, 20, 60],     # human - rouge
    7: [0, 0, 142]        # vehicle - bleu foncé
}

# Correspondance des labels avec des descriptions en majuscules
label_description = {
    0: "Void",
    1: "Flat",
    2: "Construction",
    3: "Object",
    4: "Nature",
    5: "Sky",
    6: "Human",
    7: "Vehicle"
}

legend_background_color = (0, 0, 0) 

def draw_horizontal_legend():
    rect_size = 10  
    padding = 7      
    text_offset = 120  
    font_size = 12
    
    num_columns = 4
    num_rows = (len(palette) + num_columns - 1) // num_columns
    
    legend_width = (rect_size + text_offset + padding) * num_columns
    legend_height = (rect_size + padding) * num_rows + padding
    legend = Image.new("RGB", (legend_width, legend_height), legend_background_color)
    draw = ImageDraw.Draw(legend)
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    for i, (label, color) in enumerate(palette.items()):
        row = i // num_columns
        col = i % num_columns
        x = col * (rect_size + text_offset + padding)
        y = row * (rect_size + padding)
        draw.rectangle([x + padding, y + padding, x + padding + rect_size, y + padding + rect_size], fill=tuple(color))
        draw.text((x + padding + rect_size + padding, y + padding), label_description[label], fill="black", font=font)
    
    return legend

st.title("Segmentation d'Images pour Voiture Autonome")

uploaded_file = st.file_uploader("Choisissez une image JPEG ou PNG", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    logging.info("Image uploaded")
    image = Image.open(uploaded_file)
    st.image(image, caption='Image téléchargée', use_column_width=True)
    
    if st.button("Segmenter l'image"):
        logging.info("Segmentation button clicked")
        mask_image = get_mask(image)
        if mask_image:
            legend = draw_horizontal_legend()
            st.image(legend, caption='Légende', use_column_width=True)
            st.image(mask_image, caption='Masque de segmentation', use_column_width=True)
        else:
            logging.error("Mask image is None")
