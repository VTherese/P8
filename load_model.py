import os
from azure.storage.blob import BlobServiceClient

# Variables d'environnement
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
model_blob_name = "model.keras"
model_file_path = "api/model.keras"

def download_blob_to_file(container_name, blob_name, file_name, connection_string):
    # Augmenter les délais d'attente et créer BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string, retry_total=10, timeout=600)
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)

    if os.path.exists(file_name):
        print(f"{file_name} already exists locally. Skipping download.")
        return

    try:
        with open(file_name, "wb") as file:
            file.write(blob_client.download_blob().readall())
        print(f"Successfully downloaded {blob_name} to {file_name}")
    except Exception as e:
        print(f"Failed to download {blob_name}: {str(e)}")
        raise e

# Appel de la fonction pour télécharger le fichier
download_blob_to_file(container_name, model_blob_name, model_file_path, connect_str)