import os
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

class ABlob:
    def __init__(self):
        connection_string = os.getenv("AZURE_SAK")  # ¡Sin load_dotenv!
        container_name = os.getenv("AZURE_STORAGE_CONTAINER")
        
        if not connection_string or not container_name:
            raise ValueError("Faltan variables de entorno: AZURE_SAK o AZURE_STORAGE_CONTAINER")
        
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def generate_sas(self, id: int):
        blob_name = f"poke_report_{id}.csv"
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=self.container_client.container_name,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        return sas_token
    
    def delete_blob(self, id: int) -> dict:
        blob_name = f"poke_report_{id}.csv"

        try:
            blob_client = self.blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
            blob_client.delete_blob()
            return {
                "success": True,
                "message": f"Blob '{blob_name}' eliminado correctamente."
            }

        except ResourceNotFoundError:
            return {
                "success": False,
                "message": f" El blob '{blob_name}' no existe."
            }

        except HttpResponseError   as e:
            return {
                "success": False,
                "message": f"Error de Azure al eliminar el blob '{blob_name}': {str(e)}"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f" Error inesperado al eliminar el blob '{blob_name}': {str(e)}"
            }