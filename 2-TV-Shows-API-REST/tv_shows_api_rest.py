import os
from dotenv import load_dotenv
import requests
from concurrent.futures import ThreadPoolExecutor
import pyspark

NO_SHOWS_FOUND_MESSAGE = "No shows found for the specified genre"

# Funciones para obtener los datos de los shows

def fetch_first_data_page_and_service_metadata(base_url) -> tuple[list[dict], dict]:
    response = requests.get(base_url).json()
    return response['data'], {"total_shows_amount": response['total'], "total_pages_amount": response['total_pages']}

def fetch_tv_shows_data() -> list[dict]:
    # Cargado de la url base de la API como variable de entorno
    load_dotenv()
    base_url = os.getenv("TV_SHOWS_API_BASE_URL")

    # Consulto la primera pagina para obtener la metadata asociada a la paginacion de los shows en el servicio
    # Esto permite conocer, principalmente, la cantidad total de paginas y la cantidad total de shows
    tv_shows_data, service_metadata = fetch_first_data_page_and_service_metadata(base_url)

    # Inicio el iterador desde la segunda pagina, ya que la primera request ya fue realizada
    # Utilizo la metadata aportada por el servicio para definir la cota superior de paginas a consultar
    lower_page_bound, upper_page_bound = 2, service_metadata["total_pages_amount"] + 1

    # Función a ejecutar en paralelo que permite obtener los datos de una página
    def fetch_single_data_page(page_number: int) -> list[dict]:
        response = requests.get(f"{base_url}?page={page_number}")
        return response.json()['data']

    # Ejecucion en paralelo de las requests para obtener los datos de las paginas restantes
    # Los resultados luego extienden el array original de shows
    with ThreadPoolExecutor() as executor:
        tv_shows_data.extend([
            show for page in executor.map(fetch_single_data_page, range(lower_page_bound, upper_page_bound)) for show in page
        ])

    return tv_shows_data


# Funciones para obtener el mejor show de un genero

# Enfoque utilizando List Comprehension y funciones built-in
def best_in_genre(genre: str) -> str:
    # Obtengo los datos de los shows
    raw_tv_shows_data = fetch_tv_shows_data()

    # Parseo el formato nativo del campo 'genre' de un string de generos a una lista de generos en lowercase y sin espacios
    parsed_tv_shows_data = [
        {**show, 'genre': [sub_genre.lower().replace(' ', '') for sub_genre in show['genre'].split(',')]}
        for show in raw_tv_shows_data
    ]

    # Genero un array con los shows que coinciden con el genero especificado
    shows_matched_by_genre = [show for show in parsed_tv_shows_data if genre.lower() in show['genre']]

    # Si no hay shows que coincidan con el genero especificado, devuelvo un mensaje de error
    if not shows_matched_by_genre:
        return NO_SHOWS_FOUND_MESSAGE

    # Obtengo el show con la mejor calificacion y, en caso de empate, utilizo un criterio alfabetico
    best_show = shows_matched_by_genre[0]
    for show in shows_matched_by_genre[1:]:
        if show['imdb_rating'] == best_show['imdb_rating']:
            best_show = show if show['name'] < best_show['name'] else best_show
        else:
            best_show = show if show['imdb_rating'] > best_show['imdb_rating'] else best_show

    return best_show['name']



# Enfoque utilizando Spark / Map-Reduce
def show_reducing_function(show_a, show_b):
    if show_a['imdb_rating'] == show_b['imdb_rating']:
        return show_a if show_a['name'] < show_b['name'] else show_b
    return show_a if show_a['imdb_rating'] > show_b['imdb_rating'] else show_b

def best_in_genre_spark(genre: str) -> str:
    raw_tv_shows_data = fetch_tv_shows_data()

    # Inicializacion del contexto de Spark
    conf = pyspark.SparkConf().setAppName("TVShowsApp").setMaster("local")
    sc = pyspark.SparkContext(conf=conf)

    # Creacion del RDD a partir de los datos de los shows
    shows_rdd = sc.parallelize(raw_tv_shows_data)

    # Parseo del formato original del campo 'genre' al mismo formato que en el enfoque anterior
    # Filtrado de los shows que no coinciden con el genero especificado
    shows_in_genre =  (
        shows_rdd
            .map(lambda x: {**x, 'genre': [sub_genre.lower().replace(' ', '') for sub_genre in x['genre'].split(',')]})
            .filter(lambda x: genre.lower() in x['genre'])
    )

    if shows_in_genre.isEmpty():
        sc.stop()
        return NO_SHOWS_FOUND_MESSAGE

    # Reduccion de los shows para obtener el show con la mejor calificacion y, en caso de empate, utilizar un criterio alfabetico
    best_show = shows_in_genre.reduce(lambda x, y: show_reducing_function(x, y))
    sc.stop()

    return best_show['name']
