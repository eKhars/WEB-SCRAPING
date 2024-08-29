import time
import os
from config.database import connect_to_mongodb
from scraping.mercadolibre import scrape_mercadolibre
from scraping.coppel import scrape_coppel
from scraping.ebay import scrape_ebay
from services.db_service import store_in_db, determinar_categoria
from dotenv import load_dotenv
import logging

# Configura el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def main():
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    cluster = os.getenv("MONGODB_CLUSTER")
    database_name = os.getenv("MONGODB_DATABASE")

    client = connect_to_mongodb(username, password, cluster, database_name)
    db = client[database_name]

    colecciones = {
        "Tablets": db['Tablets'],
        "Telefonos": db['Telefonos'],
        "Computadoras": db['Computadoras'],
        "Audifonos": db['Audifonos']
    }

    for collection in colecciones.values():
        collection.create_index("titulo", unique=True)

    try:
        while True:
            plataformas = [
               ('Mercado Libre', scrape_mercadolibre),
               ('Coppel', scrape_coppel),
               ('eBay', scrape_ebay)
            ]
            
            for nombre, funcion in plataformas:
                print(f"Iniciando scraping de {nombre}")
                productos = funcion()
                if productos:
                    for producto in productos:
                        if 'titulo' in producto and producto['titulo']:  # Asegúrate de que el título exista y no esté vacío
                            categoria = determinar_categoria(producto['titulo'])
                            if categoria in colecciones:
                                store_in_db(colecciones[categoria], producto)
                            else:
                                logger.info(f"Categoría no determinada para el producto: {producto['titulo']}")
                        else:
                            logger.warning("Producto sin título encontrado, no se puede categorizar")
                else:
                    print(f"No se obtuvieron productos de {nombre}")
            
            print("Ciclo de scraping completo. Esperando antes de reiniciar...")
            time.sleep(6000)  
    except KeyboardInterrupt:
        print("Proceso detenido manualmente desde la terminal.")
    finally:
        client.close()
        print("Conexión a MongoDB cerrada")

if __name__ == "__main__":
    main()
