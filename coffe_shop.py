import requests
import os
from dotenv import load_dotenv
# Esta libreria es la "regla" con la que podemos medir la distancia entre dos nodos
# usando la cantidad de palabras en común que comparten
from difflib import SequenceMatcher
# GET - Nos da la información
# POST - Escribimos datos nuevos
# DELETE - Eliminamos basura
# PUT - Actualizamos datos

# Cargamos las variables del archivo al entorno y la sobreescribimos si modificamos el API constantemente
load_dotenv(override=True)

# Obtenemos la variable específica
api_key = os.getenv("SECRET_API_KEY")

baseurl = 'https://api.spoonacular.com/'
endpoint = 'food/menuItems/search'
def main_request(baseurl, endpoint, api, busqueda):
    # Manualmente
    """
    response = requests.get(baseurl + endpoint + f"?apiKey={api}&query={busqueda}")
    """
    # Creamos un diccionario con los parametros para no hacerlo "Manualmente"
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
        self.tokens = []
    
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

# DEFINICIÓN DE STOPWORDS
# Usamos un 'set' {} porque buscar aquí es instantáneo.
# Estas palabras son ruido específico de menús de comida/café.
STOPWORDS = {
    "oz", "lb", "w/", "with", "&", "and", "the", "a", "of", 
    "nsa", "bag", "box", "served", "choice", "side", "NSA",
    "guilt-free",
}
"""def obtener_keys(texto):
        palabras_validas = set()
        # --- PASO 1: TOKENIZATION (Romper) ---
        # A. Normalizar: Convertir todo a minúsculas para que "Mocha" == "mocha"
        # B. Limpiar puntuación básica (quitamos comas que suelen pegarse a las palabras)
        texto_limpio = texto.nombre.lower().replace(",", "").replace("(", "").replace(")", "")
        # C. Tokenizar: .split() corta el texto donde haya espacios
        tokens = texto_limpio.split() 
        # Ejemplo: "iced mocha w/ soy" -> ['iced', 'mocha', 'w/', 'soy']
        # --- PASO 2: FILTERING (El Colador) ---
        for palabra in tokens:
            # Verificamos dos cosas:
            # 1. Que NO sea una stopword.
            # 2. Que NO sea un número (ej. "16" de 16 oz). .isalpha() ayuda a esto.
            if palabra not in STOPWORDS and (not palabra[0].isdigit() or "%" in palabra):
                palabras_validas.append(palabra)
        return palabras_validas
        """

def crear_indice_invertido(lista_nodos):
    """
    Recibe: Una lista de objetos ProductoNodo.
    Devuelve: Un diccionario { 'palabra_clave': [nodo1, nodo2, ...] }
    """
    indice = {}
    for nodo in lista_nodos:
        # --- PASO 1: TOKENIZATION (Romper) ---
        # A. Normalizar: Convertir todo a minúsculas para que "Mocha" == "mocha"
        nombre_lower = nodo.nombre.lower()
        # B. Limpiar puntuación básica (quitamos comas que suelen pegarse a las palabras)
        nombre_limpio = nombre_lower.replace(",", "").replace("(", "").replace(")", "")
        # C. Tokenizar: .split() corta el texto donde haya espacios
        nodo.tokens = nombre_limpio.split()
        # Ejemplo: "iced mocha w/ soy" -> ['iced', 'mocha', 'w/', 'soy']
        # --- PASO 2: FILTERING (El Colador) ---
        for palabra in nodo.tokens:
            # Verificamos:
            # 1. Que NO sea una stopword.
            # 2. Que NO sea un número (ej. "16" de 16 oz). .isalpha() ayuda a esto.
            if palabra not in STOPWORDS and (not palabra[0].isdigit() or "%" in palabra):
                # --- PASO 3: INDEXACIÓN (Guardar) ---
                # Si la palabra es nueva en el índice, creamos su lista vacía
                if palabra not in indice:
                    indice[palabra] = []
                # Agregamos el NODO actual a la lista de esa palabra
                # Importante: Guardamos el OBJETO nodo, no solo su ID o nombre
                indice[palabra].append(nodo)
    return indice

def calcular_peso(texto_a, texto_b):
    # La biblioteca SequenceMatcher devuelve un float entre 0.0 (nada que ver) - 1.0 (idénticos)
    similitud = SequenceMatcher(None, texto_a, texto_b).ratio()
    # Invertimos para Dijikstra
    # Convertimos 0.9 (Alta similitud) -> 0.1 (Camino corto)
    peso = 1.0 - similitud
    return peso

def conectar_grafo(lista_nodos, indice_invertido):
    # Recorremos cada producto de nuestra API
    for nodo_actual in lista_nodos:
        candidatos = set() # Usamos un set para evitar duplicados
        for palabra in nodo_actual.tokens:
            if palabra not in STOPWORDS and (not palabra[0].isdigit() or "%" in palabra):
                if palabra in indice_invertido:
                    # Agregamos TODOS los nodos potenciales de esa palabra a nuestros candidatos
                    lista_vecinos_potenciales = indice_invertido[palabra]
                    candidatos.update(lista_vecinos_potenciales)
        # Eliminamos el nodo de vecinos, un nodo no puede ser su propio vecino
        candidatos.discard(nodo_actual)

        # Calculamos el peso y conectamos
        for vecino in candidatos:
            peso = calcular_peso(nodo_actual.nombre, vecino.nombre)
            # Ignoramos valores casi nada iguales
            # Guardamos la Tupla (Nodo, peso)
            nodo_actual.vecinos.append((vecino, peso))


# guardamos en "data" el texto formato json
data = main_request(baseurl, endpoint, api_key, "coffe")
nodos = parse_json(data)
indiceInvertido = crear_indice_invertido(nodos)
#print(indiceInvertido)
primer_nodo = nodos[0]
conectar_grafo(nodos, indiceInvertido)
