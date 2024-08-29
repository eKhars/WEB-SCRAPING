import logging
from pymongo import errors

logger = logging.getLogger(__name__)

def determinar_categoria(titulo):
    titulo = titulo.lower()
    categorias = {
        "tablets": [
            "tablet", "ipad", "galaxy tab", "surface", "fire", "lenovo tab", "huawei matepad", "xperia tablet", "tableta"
        ],
        "telefonos": [
            "telefono", "smartphone", "celular", "iphone", "samsung", "xiaomi", "oneplus", "motorola",
            "sony", "lg", "nokia", "realme", "oppo", "asus", "huawei", "vivo"
        ],
        "computadoras": [
            "computadora", "laptop", "pc", "notebook", "macbook", "lenovo", "dell", "hp", "asus", "acer",
            "msi", "razer", "samsung", "surface laptop", "apple"
        ],
        "audifonos": [
            "audifonos", "auricular", "headphones", "earphones", "beats", "sony", "bose", "sennheiser", 
            "jabra", "skullcandy", "jbl", "apple airpods", "anker", "plantronics", "bang & olufsen", "Audífonos"
        ]
    }
    
    for categoria, palabras_clave in categorias.items():
        if any(palabra in titulo for palabra in palabras_clave):
            return categoria.capitalize()

    return None

def store_in_db(collection, producto):
    try:
        collection.insert_one(producto)
        logger.info(f"Producto insertado: {producto['titulo']}")
    except errors.DuplicateKeyError:
        logger.info(f"Producto duplicado no insertado: {producto['titulo']}")
    except Exception as e:
        logger.error(f"Error al insertar en la base de datos: {e}")
