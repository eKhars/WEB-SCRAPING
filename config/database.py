import urllib.parse
import logging
import time
from pymongo import MongoClient, errors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_mongodb(username, password, cluster, database_name, retries=5, delay=5):
    uri = f"mongodb+srv://{username}:{password}@{cluster}/{database_name}?retryWrites=true&w=majority"
    for i in range(retries):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            logger.info("Conexión exitosa a MongoDB Atlas!")
            return client
        except errors.ServerSelectionTimeoutError as e:
            logger.error(f"Intento {i+1}/{retries}: Error al conectar a MongoDB: {e}")
            time.sleep(delay)
    raise Exception("No se pudo conectar a MongoDB después de varios intentos")
