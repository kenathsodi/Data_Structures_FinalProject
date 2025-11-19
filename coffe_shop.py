import requests
import os
from dotenv import load_dotenv
# GET - Nos da la información
# POST - Escribimos datos nuevos
# DELETE - Eliminamos basura
# PUT - Actualizamos datos
# Cargamos las variables del archivo al entorno y la sobreescribimos si modificamos el API constantemente
load_dotenv(override=True)

# Obtenemos la variable específica
api_key = os.getenv("SECRET_API_KEY")

baseurl = 'https://api.spoonacular.com/food/'
endpoint = 'menuItems/search'
def main_request(baseurl, endpoint, api, busqueda):
    # Manualmente
    """
    response = requests.get(baseurl + endpoint + f"?apiKey={api}&query={busqueda}")
    """
    # Creamos un diccionario con los parametros para no hacer lo "Manualmente"
    parametros ={
        "apiKey": api,
        "query": busqueda,
    }
    # Guardamos la respuesta
    response = requests.get(baseurl + endpoint, params=parametros)
    # Convertimos la respuesta a json
    return response.json()

# Inicializamos los nodos para después hacer comparativas
class ProductosNodo:
    def __init__(self, id_producto, nombre):
        self.id_producto = id_producto
        self.nombre = nombre
        self.vecinos = []
    
    # Sin esta función no es légible nuestra lista (con los productos)
    # nos muestra las direcciones donde se almacenan en vez de los strings o int
    def __repr__(self):
        return f"<{self.nombre} (ID: {self.id_producto})"

# Creamos una lista y vamos añadiendo nuestros productos con id y nombre
def parse_json(response):
    nodos = []
    for item in response['menuItems']:
        nuevo_nodo = ProductosNodo(item['id'], item['title'])
        nodos.append(nuevo_nodo)
    return nodos

# guardamos en "data" el texto formato json
data = main_request(baseurl, endpoint, api_key, "coffe")
# Imprimimos la lista
print(parse_json(data))
