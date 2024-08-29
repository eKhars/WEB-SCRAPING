import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

# Lista de marcas comunes
marcas_comunes = [
    "Sony", "Bose", "Sennheiser", "JBL", "Beats", "Apple", "Audio-Technica", "Skullcandy",
    "AKG", "Bang & Olufsen", "Shure", "Plantronics", "Logitech", "Philips", "Pioneer", 
    "Samsung", "Turtle Beach", "Beyerdynamic", "HyperX", "Razer", "Marshall", "1MORE", "Creative",
    "Jabra", "RHA", "Klipsch", "Sennheiser", "Meze", "Edifier", "Cowin", "Harman Kardon", "Focal",
    "Xiaomi", "Huawei", "OnePlus", "Google", "Motorola", "Nokia", "Oppo", "Vivo", "Realme", "LG",
    "Asus", "ZTE", "Honor", "Alcatel", "Lenovo", "BlackBerry", "Infinix", "Tecno", "Meizu", "Doogee",
    "Fairphone", "Essential", "Sharp", "Panasonic", "Sagem", "Caterpillar", "Dell", "HP", "Lenovo",
    "Acer", "Microsoft", "Samsung", "Razer", "MSI", "Toshiba", "LG", "Huawei", "Google", "Sony",
    "Gigabyte", "Alienware", "Chuwi", "XPS", "Clevo", "Origin PC", "System76", "Dynabook", "Eurocom",
    "Panasonic", "Amazon", "Asus", "Acer", "Sony", "Xiaomi", "Nokia", "Google", "Chuwi", "Alldocube",
    "TCL", "Wacom", "ZTE", "HP", "Dell", "LG", "Panasonic", "Cube", "Vankyo", "ONN", "Kobo", "E Fun", "Ematic"
]

def extraer_marca(titulo):
    for marca in marcas_comunes:
        if marca.lower() in titulo.lower():
            return marca
    return "Marca desconocida"

def scrape_coppel():
    categorias_urls = {
        "Tablets": {
            "url": "https://www.coppel.com/tablets",
            "item_class": "chakra-card css-18e7glt",
            "title_class": "chakra-text css-1g6dv0g",
            "price_class": "chakra-text css-1uqwphq",
            "envio_class": "",
            "calificacion_class": "",
            "image_class": "css-19y8pwk",  # Clase del <picture>
            "redireccion_class": "chakra-card__body css-3439hj"
        },
        "Telefonos": {
            "url": "https://www.coppel.com/equipos-celulares",
            "item_class": "chakra-card css-18e7glt",
            "title_class": "chakra-text css-1g6dv0g",
            "price_class": "chakra-text css-1uqwphq",
            "envio_class": "",
            "calificacion_class": "",
            "image_class": "css-19y8pwk",  # Clase del <picture>
            "redireccion_class": "chakra-card__body css-3439hj"
        },
        "Computadoras": {
          "url": "https://www.coppel.com/laptops",
             "item_class": "chakra-card css-18e7glt",
            "title_class": "chakra-text css-1g6dv0g",
            "price_class": "chakra-text css-1uqwphq",
            "envio_class": "",
            "calificacion_class": "",
            "image_class": "css-19y8pwk",  # Clase del <picture>
            "redireccion_class": "chakra-card__body css-3439hj"
        },
        "Audifonos": {
          "url": "https://www.coppel.com/audifonos",
           "item_class": "chakra-card css-18e7glt",
            "title_class": "chakra-text css-1g6dv0g",
            "price_class": "chakra-text css-1uqwphq",
            "envio_class": "",
            "calificacion_class": "",
            "image_class": "css-19y8pwk",  # Clase del <picture>
            "redireccion_class": "chakra-card__body css-3439hj"
        }
    }

    productos = []

    for categoria, data in categorias_urls.items():
        response = requests.get(data["url"])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', class_=data["item_class"])

            for item in items:
                producto = {}
                titulo = item.find('h3', class_=data["title_class"])
                precio = item.find('span', class_=data["price_class"])
                envio = item.find('span', class_=data.get("envio_class"))
                calificacion = item.find('span', class_=data.get("calificacion_class"))
                redireccion = item.find('a', class_=data.get("redireccion_class"))

                if titulo:
                    titulo_text = titulo.text.strip()
                    producto['titulo'] = titulo_text

                    # Extraer la marca del título
                    producto['marca'] = extraer_marca(titulo_text)

                if precio:
                    producto['precio'] = precio.text.strip()
                if envio:
                    producto['envio'] = envio.text.strip()
                if calificacion:
                    producto['calificacion'] = calificacion.text.strip()
                if redireccion:
                    # Convertir la URL relativa a una URL completa
                    producto['url'] = urljoin(data["url"], redireccion.get('href'))

                # Obtener la URL de la imagen
                picture = item.find('picture', class_=data["image_class"])
                if picture:
                    img_tag = picture.find('img')
                    if img_tag and img_tag.get('src'):
                        producto['imagen_url'] = img_tag['src']
                    elif img_tag and img_tag.get('data-src'):
                        producto['imagen_url'] = img_tag['data-src']
                    else:
                        # Si no hay src en el <img>, intenta con <source>
                        source_tag = picture.find('source')
                        if source_tag and source_tag.get('srcset'):
                            producto['imagen_url'] = source_tag['srcset'].split()[0]

                producto['plataforma'] = 'Coppel'
                producto['categoria'] = categoria
                productos.append(producto)
        else:
            logger.error(f"Error al obtener la página de {categoria} en Coppel, código de error: {response.status_code}")

    return productos
