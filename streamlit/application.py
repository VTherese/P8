import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# URL de l'API Flask
FLASK_API_URL = "http://127.0.0.1:5000/segment"

def get_mask(image):
    buffered = BytesIO()
    image.save(buffered, format=image.format)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # Correction pour envoyer l'image en base64 via JSON
    response = requests.post(FLASK_API_URL, json={'image': img_str})
    
    if response.status_code == 200:
        mask_base64 = response.json()["mask"]
        mask_data = base64.b64decode(mask_base64)
        mask_image = Image.open(BytesIO(mask_data))
        return mask_image
    else:
        st.error("Erreur lors de la requête à l'API Flask")
        return None

st.title("Segmentateur d'Images")

uploaded_file = st.file_uploader("Choisissez une image JPEG ou PNG", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Image téléchargée', use_column_width=True)
    
    if st.button("Segmenter l'image"):
        mask_image = get_mask(image)
        if mask_image:
            st.image(mask_image, caption='Masque de segmentation', use_column_width=True)
