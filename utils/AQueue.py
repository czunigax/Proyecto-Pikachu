import os
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy
from dotenv import load_dotenv

load_dotenv()

class AQueue:
    def __init__(self):
        self.azure_sak = os.getenv("AZURE_SAK")
        self.queue_name = os.getenv("QUEUE_ACTIVATE")
        self.queue_client = QueueClient.from_connection_string(self.azure_sak, self.queue_name)
        self.queue_client.message_encode_policy = BinaryBase64EncodePolicy()
        self.queue_client.message_decode_policy = BinaryBase64DecodePolicy()
        
    async def insert_message(self, message: str):
        message_bytes = message.encode('utf-8')  # corregido 'enconde' → 'encode'
        encoded_message = self.queue_client.message_encode_policy.encode(message_bytes)
        self.queue_client.send_message(encoded_message)
