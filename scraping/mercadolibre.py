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

def scrape_mercadolibre():
    categorias_urls = {
        "Tablets": {
            "url": "https://listado.mercadolibre.com.mx/tablets#D[A:tablets]",
            "item_class": "ui-search-result__wrapper",
            "title_class": "ui-search-item__title",
            "price_class": "andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript",
            "image_class": "ui-search-result-image__element",
            "envio_class": "ui-pb-highlight",
            "calificacion_class": "andes-visually-hidden",
            "redireccion_class": "ui-search-item__group__element ui-search-link__title-card ui-search-link"
        },
        "Telefonos": {
            "url": "https://listado.mercadolibre.com.mx/telefonos#D[A:telefonos]",
            "item_class": "ui-search-result__wrapper",
            "title_class": "ui-search-item__title",
            "price_class": "andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript",
            "image_class": "ui-search-result-image__element",
            "envio_class": "ui-pb-highlight",
            "calificacion_class": "andes-visually-hidden",
            "redireccion_class": "ui-search-item__group__element ui-search-link__title-card ui-search-link"
        },
        "Computadoras": {
          "url": "https://listado.mercadolibre.com.mx/laptops#D[A:laptops]",
            "item_class": "ui-search-result__wrapper",
            "title_class": "ui-search-item__title",
            "price_class": "andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript",
            "image_class": "ui-search-result-image__element",
            "envio_class": "ui-pb-highlight",
            "calificacion_class": "andes-visually-hidden",
            "redireccion_class": "ui-search-item__group__element ui-search-link__title-card ui-search-link"
        },
        "Audifonos": {
          "url": "https://listado.mercadolibre.com.mx/audifonos#D[A:audifonos]",
            "item_class": "ui-search-result__wrapper",
            "title_class": "ui-search-item__title",
            "price_class": "andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript",
            "image_class": "ui-search-result-image__element",
            "envio_class": "ui-pb-highlight",
            "calificacion_class": "andes-visually-hidden",
            "redireccion_class": "ui-search-item__group__element ui-search-link__title-card ui-search-link"
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
                titulo = item.find('h2', class_=data["title_class"])
                precio = item.find('span', class_=data["price_class"])
                imagen = item.find('img', class_=data["image_class"])
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
                if imagen:
                    imagen_url = imagen.get('src')
                    if not imagen_url or imagen_url.startswith("data:image"):
                        imagen_url = imagen.get('data-src')
                    producto['imagen_url'] = imagen_url

                producto['plataforma'] = 'Mercado Libre'
                producto['categoria'] = categoria
                productos.append(producto)
        else:
            logger.error(f"Error al obtener la página de {categoria} en MercadoLibre, código de error: {response.status_code}")

    return productos
