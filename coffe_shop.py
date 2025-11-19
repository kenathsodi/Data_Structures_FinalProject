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
    response = requests.get(baseurl + endpoint, params=parametros)
    return response.json()

class productosNodo:
    print("")

print(main_request(baseurl, endpoint, api_key, "coffe"))
"""def parsce_json(response):
    list_provisional = []
    for item in response:
        products = {
            'id': item['id'],
            'name': item['title'],
            'ingredients' : item['ingredients'],
        }
        list_provisional.append(products)
    return list_provisional

data = main_request(baseurl, endpoint)
print(data)
#print(data[0]['title'])
#print(parsce_json(data))
"""
