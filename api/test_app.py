import pytest
from flask import Flask
from io import BytesIO
import base64
import json
from PIL import Image
import numpy as np
from app import app

# Créer une fixture pour le client de test Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_check(client):
    rv = client.get('/health')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data['status'] == 'Healthy'

def test_segment(client):
    # Créer une image de test
    image = Image.new('RGB', (256, 256), color='red')
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Préparer les données pour la requête POST
    data = json.dumps({"image": img_str})
    headers = {'Content-Type': 'application/json'}

    rv = client.post('/segment', data=data, headers=headers)
    json_data = rv.get_json()
    
    assert rv.status_code == 200
    assert 'mask' in json_data

    # Vérifier que le masque renvoyé est bien une image
    mask_base64 = json_data['mask']
    mask_data = base64.b64decode(mask_base64)
    mask_image = Image.open(BytesIO(mask_data))

    assert mask_image.size == (256, 256)
    assert mask_image.mode == 'RGB'

