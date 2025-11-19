# Rick and Morty example project
import requests
baseurl = 'https://rickandmortyapi.com/api/' # Asignamos el url a base url
endpoint = 'character' # Añadimos la extensión /character al url

def main_request(baseurl, endpoint, x): # "x" es el número de página con el que queremos trabajar
                                    # la extensión del url es "?page=(el número de página)"
    r = requests.get(baseurl + endpoint + f'?page={x}') # pedimos https://rickandmortyapi.com/api/character/?page=x
    return r.json() # Nos devuelve la info total del API, si no tuviera ".json" nos devolvería <200>

def get_pages(data):
    return data['info']['pages'] # Nos devuelve las páginas del API

def parsce_json(response):
    # Creamos una lista para poder devolver el diccionario en esta función
    character_list = []
    for item in response['results']:
        characters = {
            #Creamos un diccionario para operar con los datos, sino no podemos
            'name': item['name'], 
            'no_episodes': len(item['episode']),
        }
        character_list.append(characters) # Guardamos cada personaje en la lista
    return character_list

data = main_request(baseurl, endpoint, 3)
parsce_json(data)
print(parsce_json(data))
#rickSanchez = data['results'][0]['name']
#episodesRicksanchez = data['results'][0]['episode']
#print(len(episodesRicksanchez))
