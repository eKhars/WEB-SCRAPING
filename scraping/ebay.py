import requests
from bs4 import BeautifulSoup
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

def scrape_ebay():
    categorias_urls = {
        "Tablets": {
            "url": "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2499334.m570.l1313&_nkw=tablets&_sacat=0",
            "item_class": "s-item__wrapper clearfix",
            "title_class": "s-item__title",
            "price_class": "s-item__price",
            "image_wrapper_class": "s-item__image-wrapper image-treatment",  
            "envio_class": "s-item__shipping s-item__logisticsCost",
            "calificacion_class": "s-item__reviews-count",
            "redireccion_class": "s-item__link"
        },
        "Telefonos": {
            "url": "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=telefono&_sacat=0",
            "item_class": "s-item__wrapper clearfix",
            "title_class": "s-item__title",
            "price_class": "s-item__price",
            "image_wrapper_class": "s-item__image-wrapper image-treatment",  
            "envio_class": "s-item__shipping s-item__logisticsCost",
            "calificacion_class": "s-item__reviews-count",
            "redireccion_class": "s-item__link"
        },
        "Computadoras": {
            "url": "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=laptop&_sacat=0",
            "item_class": "s-item__wrapper clearfix",
            "title_class": "s-item__title",
            "price_class": "s-item__price",
            "image_wrapper_class": "s-item__image-wrapper image-treatment",  
            "envio_class": "s-item__shipping s-item__logisticsCost",
            "calificacion_class": "s-item__reviews-count",
            "redireccion_class": "s-item__link"
        },
        "Audifonos": {
            "url": "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=audifonos&_sacat=0",
            "item_class": "s-item__wrapper clearfix",
            "title_class": "s-item__title",
            "price_class": "s-item__price",
            "image_wrapper_class": "s-item__image-wrapper image-treatment",  
            "envio_class": "s-item__shipping s-item__logisticsCost",
            "calificacion_class": "s-item__reviews-count",
            "redireccion_class": "s-item__link"
        }
    }

    productos = []

    for categoria, data in categorias_urls.items():
        try:
            response = requests.get(data["url"])
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', class_=data["item_class"])

            for item in items:
                producto = {}
                titulo = item.find('div', class_=data["title_class"])
                precio = item.find('span', class_=data["price_class"])
                imagen_wrapper = item.find('div', class_=data["image_wrapper_class"])  # Buscar el div que contiene la imagen
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
                    producto['url'] = redireccion.get('href')
                if imagen_wrapper:
                    imagen = imagen_wrapper.find('img')  # Obtener la imagen dentro del div
                    if imagen:
                        imagen_url = imagen.get('src')  # Obtener la URL de la imagen
                        if not imagen_url or imagen_url.startswith("data:image"):
                            imagen_url = imagen.get('data-src')
                        producto['imagen_url'] = imagen_url

                producto['plataforma'] = 'eBay'
                producto['categoria'] = categoria
                productos.append(producto)
        except requests.RequestException as e:
            logger.error(f"Error al obtener la página de {categoria} en eBay: {e}")
        except Exception as e:
            logger.error(f"Error al procesar los datos de la categoría {categoria}: {e}")

    return productos
