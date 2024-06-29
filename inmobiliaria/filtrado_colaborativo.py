<<<<<<< HEAD
import requests
import psycopg2
import json
import math
import itertools
import pandas as pd
from psycopg2 import sql
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.response import Response

# Constants
URL_API = 'https://arqui-sistema-recomendacion-85b7038cdf33.herokuapp.com/api/inmueblesPorUsuario/get_filtro/'
URL_API_INMUEBLES = 'https://arqui-sistema-recomendacion-85b7038cdf33.herokuapp.com/api/inmuebles/'
URL_API_LOGIN = 'https://arqui-sistema-recomendacion-85b7038cdf33.herokuapp.com/api/login/'
URL_API_PREFERENCIAS = 'https://arqui-sistema-recomendacion-85b7038cdf33.herokuapp.com/api/interesesPorUsuario/'

LOGIN_DATA = {
    'username': 'diego3026',
    'password': '3174748557d'
}

DB_CONFIG = {
    'host': 'dbarquitecura.postgres.database.azure.com',
    'database': 'postgres',
    'user': 'gidsyc',
    'password': 'Semillero2024'
}

PESOS = [4, 2, 1, 3]  # [favorito, calificacion, clics, preferencia]

def normalizacion(valor, valor_maximo, valor_minimo):
    return (valor - valor_minimo) / (valor_maximo - valor_minimo)

class InmuebleUsuarioNormalizado:
    def __init__(self, inmueble, usuario, favorito, calificacion, clics, puntaje_preferencia, pesos):
        self.inmueble = inmueble
        self.usuario = usuario
        self.favorito = favorito
        self.calificacion = calificacion
        self.clics = clics
        self.pesos = pesos
        self.puntaje_preferencia = puntaje_preferencia

    def get_clasificacion(self):
        clasificacion = (
            self.pesos[0] * self.favorito +
            self.pesos[1] * self.calificacion +
            self.pesos[2] * self.clics +
            self.pesos[3] * self.puntaje_preferencia
        )
        return clasificacion

def get_token():
    response_login = requests.post(url=URL_API_LOGIN, data=LOGIN_DATA)
    if response_login.status_code == 200:
        return response_login.json()['access']
    else:
        raise Exception(f'Error en la petición login: {response_login.status_code}')

def get_datos_api(url):
    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error en la petición: {response.status_code}')

def get_datos_preferencias_por_usuario():
    return get_datos_api(URL_API_PREFERENCIAS)

def consultar_base_de_datos(query, params=None):
    try:
        conexion = psycopg2.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        cursor.execute(query, params)
        columnas = [desc[0] for desc in cursor.description]
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return columnas, resultados
    except (Exception, psycopg2.DatabaseError) as error:
        raise Exception(f'Error al acceder a la base de datos: {error}')

def procesar_intereses(preferencias):
    intereses_por_usuario = {}
    for preferencia in preferencias:
        usuario = preferencia['usuario']
        interes = preferencia['interes']
        if usuario not in intereses_por_usuario:
            intereses_por_usuario[usuario] = []
        intereses_por_usuario[usuario].append(interes)
    return intereses_por_usuario

def procesar_inmuebles(inmuebles):
    inmueble_caracteristicas = []
    for item in inmuebles:
        caracteristicas = item['caracteristicas']
        if caracteristicas:
            for caracteristica in caracteristicas:
                dato = {'id_inmueble': item['id'], 'nombre_caracteristica': caracteristica['nombre'].lower()}
                inmueble_caracteristicas.append(dato)

    inmuebles_con_caracteristicas = {}
    for key, group in itertools.groupby(
        sorted(inmueble_caracteristicas, key=lambda x: x['id_inmueble']), lambda x: x['id_inmueble']
    ):
        inmuebles_con_caracteristicas[key] = [item['nombre_caracteristica'] for item in group]
    return inmuebles_con_caracteristicas


def calcular_coincidencias(intereses_por_usuario, inmuebles_con_caracteristicas):
    coincidencias_todos_usuarios = {}
    for usuario, intereses in intereses_por_usuario.items():
        coincidencias_usuario = []
        for inmueble, caracteristicas in inmuebles_con_caracteristicas.items():
            coincidencias = [interes for interes in intereses if interes in caracteristicas]
            if coincidencias:
                coincidencias_usuario.append((inmueble, coincidencias))
        coincidencias_todos_usuarios[usuario] = coincidencias_usuario
    return coincidencias_todos_usuarios

def valores_coincidencia_por_usuario(intereses_por_usuario, max_puntaje):
    valores_por_usuarios = []
    for usuario, intereses in intereses_por_usuario.items():
        valores_por_usuarios.append({"usuario": usuario, "valorCoincidencia": (max_puntaje / len(intereses))})
    return valores_por_usuarios

def buscar_vc_usuario(vCoincidenciasPorUsuario, nUsuario):
    for usuario in vCoincidenciasPorUsuario:
        if usuario['usuario'] == nUsuario:
            return usuario
    return None

def puntajes_usuarios(coincidencias_todos_usuarios, vCoincidenciasPorUsuario):
    puntaje_por_usuarios = []
    for usuario, coincidencias in coincidencias_todos_usuarios.items():
        valorCoincidenciaUsuario = buscar_vc_usuario(vCoincidenciasPorUsuario, usuario)
        puntajes_por_inmueble = []
        if valorCoincidenciaUsuario:
            for coincidencia in coincidencias:
                puntaje = len(coincidencia[1]) * valorCoincidenciaUsuario["valorCoincidencia"]
                puntajes_por_inmueble.append({"idimueble": coincidencia[0], "puntaje": puntaje})
        puntaje_por_usuarios.append({"usuario": usuario, "puntajePorInmueble": puntajes_por_inmueble})
    return puntaje_por_usuarios

def obtener_datosLimpios(inmuebles,usuarios):
    datosLimpios = {}
    for item in usuarios:
        usuario = item[1]
        if usuario not in datosLimpios:
            datosLimpios[usuario] = {}
            for inmueble in inmuebles:
                id_inmueble = inmueble[0]
                datosLimpios[usuario][id_inmueble] = None

    return datosLimpios

def calcular_clasificaciones(datos, puntajes_por_usuarios, pesos,datosLimpios):
    calificaciones, clics, favoritos = [], [], []
    for item in datos:
        if item['calificacion']:
            calificaciones.append(item['calificacion'])
        if item['numeroDeClicks']:
            clics.append(item['numeroDeClicks'])
        if item['favorito']:
            favoritos.append(item['favorito'])

    promedio_calificaciones = sum(calificaciones) / len(calificaciones) if len(calificaciones)>0 else 1
    promedio_clics = sum(clics) / len(clics) if len(clics) else 0
    max_clics = max(clics) if len(clics) else 0
    promedio_favoritos = sum(favoritos) / len(favoritos) if len(favoritos) else 0

    for value in datos:
        id_inmueble = value['inmueble']
        usuario = value['usuario']
        calificacion = normalizacion(value['calificacion'], 5, 1) if value['calificacion'] else promedio_calificaciones
        favorito = int(value['favorito']) if value['favorito'] else promedio_favoritos
        clics = normalizacion(value['numeroDeClicks'], max_clics, 0) if value['numeroDeClicks'] and max_clics > 0 else promedio_clics

        preferencia = 0
        index_usuario = next((i for i, dic in enumerate(puntajes_por_usuarios) if dic["usuario"] == usuario), -1)
        if index_usuario != -1:
            puntajes_usuario = puntajes_por_usuarios[index_usuario]['puntajePorInmueble']
            index_inmueble = next((i for i, dic in enumerate(puntajes_usuario) if dic["idimueble"] == id_inmueble), -1)
            if index_inmueble != -1:
                preferencia = puntajes_usuario[index_inmueble]['puntaje']

        if id_inmueble and usuario:
            inmueble_por_usuario = InmuebleUsuarioNormalizado(
                inmueble=id_inmueble, usuario=usuario, calificacion=calificacion,
                favorito=favorito, clics=clics, puntaje_preferencia=preferencia, pesos=pesos
            )
            datosLimpios[usuario][id_inmueble] = inmueble_por_usuario.get_clasificacion()
    return datosLimpios

def guardar_datos(datosLimpios, nombre_archivo='datosLimpios.json'):
    with open(nombre_archivo, 'w') as archivo_json:
        json.dump(datosLimpios, archivo_json, indent=4)

def predecir_valoraciones(user, ratings_df, sim_df):
    user_ratings = ratings_df.loc[user]
    sim_scores = sim_df[user]

    sim_scores = sim_scores.drop(user)
    ratings_df = ratings_df.drop(user)

    weighted_sum = (ratings_df.T * sim_scores).sum(axis=1)
    sim_sum = sim_scores.sum()
    
    predicted_ratings = weighted_sum / sim_sum
    predicted_ratings = predicted_ratings[user_ratings.isna()]
    predicted_ratings = predicted_ratings[predicted_ratings > 0]

    return predicted_ratings.sort_values(ascending=False)

def generar_recomendaciones(usuario, datosLimpios):
    ratings_df = pd.DataFrame(datosLimpios).T
    cosine_sim = cosine_similarity(ratings_df.fillna(0))
    cosine_sim_df = pd.DataFrame(cosine_sim, index=ratings_df.index, columns=ratings_df.index)
    predicted_ratings = predecir_valoraciones(usuario, ratings_df, cosine_sim_df)
    # print(predicted_ratings)
    return predicted_ratings.index.tolist()

def main(usuario):
    # Obtener datos de la API y la base de datos
    preferencias = get_datos_preferencias_por_usuario()
    columnas, resultados_inmuebles = consultar_base_de_datos('SELECT id FROM inmobiliaria_inmueble')
    columnas_user, resultados_usuarios = consultar_base_de_datos('SELECT id, username FROM inmobiliaria_usuario')
    inmuebles = get_datos_api(URL_API_INMUEBLES)
    datos_api = get_datos_api(URL_API)

    # Procesar datos
    intereses_por_usuario = procesar_intereses(preferencias)
    inmuebles_con_caracteristicas = procesar_inmuebles(inmuebles)
    coincidencias_todos_usuarios = calcular_coincidencias(intereses_por_usuario, inmuebles_con_caracteristicas)
    vCoincidenciasPorUsuario = valores_coincidencia_por_usuario(intereses_por_usuario, 10)
    puntajes_por_usuarios = puntajes_usuarios(coincidencias_todos_usuarios, vCoincidenciasPorUsuario)
    datosLimpios = obtener_datosLimpios(resultados_inmuebles,resultados_usuarios)
    datos = calcular_clasificaciones(datos_api, puntajes_por_usuarios, PESOS,datosLimpios)
    # print(datos)
    # Guardar y generar recomendaciones
    # guardar_datos(datos)
    recomendaciones = generar_recomendaciones(usuario=usuario, datosLimpios=datos)
    return recomendaciones
=======
import requests
import psycopg2
import json
import math
import itertools
import pandas as pd
from psycopg2 import sql
from sklearn.metrics.pairwise import cosine_similarity

# Constants
URL_API = 'https://arqui-sistema-recomendacion-85b7038cdf33.herokuapp.com/api/inmueblesPorUsuario/get_filtro/'
URL_API_INMUEBLES = 'https://arqui-sistema-recomendacion-85b7038cdf33.herokuapp.com/api/inmuebles/'
URL_API_LOGIN = 'https://arqui-sistema-recomendacion-85b7038cdf33.herokuapp.com/api/login/'
URL_API_PREFERENCIAS = 'https://arqui-sistema-recomendacion-85b7038cdf33.herokuapp.com/api/interesesPorUsuario/'

LOGIN_DATA = {
    'username': 'diego3026',
    'password': '3174748557d'
}

DB_CONFIG = {
    'host': 'dbarquitecura.postgres.database.azure.com',
    'database': 'postgres',
    'user': 'gidsyc',
    'password': 'Semillero2024'
}

PESOS = [4, 2, 1, 3]  # [favorito, calificacion, clics, preferencia]

def normalizacion(valor, valor_maximo, valor_minimo):
    return (valor - valor_minimo) / (valor_maximo - valor_minimo)

class InmuebleUsuarioNormalizado:
    def __init__(self, inmueble, usuario, favorito, calificacion, clics, puntaje_preferencia, pesos):
        self.inmueble = inmueble
        self.usuario = usuario
        self.favorito = favorito
        self.calificacion = calificacion
        self.clics = clics
        self.pesos = pesos
        self.puntaje_preferencia = puntaje_preferencia

    def get_clasificacion(self):
        clasificacion = (
            self.pesos[0] * self.favorito +
            self.pesos[1] * self.calificacion +
            self.pesos[2] * self.clics +
            self.pesos[3] * self.puntaje_preferencia
        )
        return clasificacion

def get_token():
    response_login = requests.post(url=URL_API_LOGIN, data=LOGIN_DATA)
    if response_login.status_code == 200:
        return response_login.json()['access']
    else:
        raise Exception(f'Error en la petición login: {response_login.status_code}')

def get_datos_api(url):
    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error en la petición: {response.status_code}')

def get_datos_preferencias_por_usuario():
    return get_datos_api(URL_API_PREFERENCIAS)

def consultar_base_de_datos(query, params=None):
    try:
        conexion = psycopg2.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        cursor.execute(query, params)
        columnas = [desc[0] for desc in cursor.description]
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return columnas, resultados
    except (Exception, psycopg2.DatabaseError) as error:
        raise Exception(f'Error al acceder a la base de datos: {error}')

def procesar_intereses(preferencias):
    intereses_por_usuario = {}
    for preferencia in preferencias:
        usuario = preferencia['usuario']
        interes = preferencia['interes']
        if usuario not in intereses_por_usuario:
            intereses_por_usuario[usuario] = []
        intereses_por_usuario[usuario].append(interes)
    return intereses_por_usuario

def procesar_inmuebles(inmuebles):
    inmueble_caracteristicas = []
    for item in inmuebles:
        caracteristicas = item['caracteristicas']
        if caracteristicas:
            for caracteristica in caracteristicas:
                dato = {'id_inmueble': item['id'], 'nombre_caracteristica': caracteristica['nombre'].lower()}
                inmueble_caracteristicas.append(dato)

    inmuebles_con_caracteristicas = {}
    for key, group in itertools.groupby(
        sorted(inmueble_caracteristicas, key=lambda x: x['id_inmueble']), lambda x: x['id_inmueble']
    ):
        inmuebles_con_caracteristicas[key] = [item['nombre_caracteristica'] for item in group]
    return inmuebles_con_caracteristicas


def calcular_coincidencias(intereses_por_usuario, inmuebles_con_caracteristicas):
    coincidencias_todos_usuarios = {}
    for usuario, intereses in intereses_por_usuario.items():
        coincidencias_usuario = []
        for inmueble, caracteristicas in inmuebles_con_caracteristicas.items():
            coincidencias = [interes for interes in intereses if interes in caracteristicas]
            if coincidencias:
                coincidencias_usuario.append((inmueble, coincidencias))
        coincidencias_todos_usuarios[usuario] = coincidencias_usuario
    return coincidencias_todos_usuarios

def valores_coincidencia_por_usuario(intereses_por_usuario, max_puntaje):
    valores_por_usuarios = []
    for usuario, intereses in intereses_por_usuario.items():
        valores_por_usuarios.append({"usuario": usuario, "valorCoincidencia": (max_puntaje / len(intereses))})
    return valores_por_usuarios

def buscar_vc_usuario(vCoincidenciasPorUsuario, nUsuario):
    for usuario in vCoincidenciasPorUsuario:
        if usuario['usuario'] == nUsuario:
            return usuario
    return None

def puntajes_usuarios(coincidencias_todos_usuarios, vCoincidenciasPorUsuario):
    puntaje_por_usuarios = []
    for usuario, coincidencias in coincidencias_todos_usuarios.items():
        valorCoincidenciaUsuario = buscar_vc_usuario(vCoincidenciasPorUsuario, usuario)
        puntajes_por_inmueble = []
        if valorCoincidenciaUsuario:
            for coincidencia in coincidencias:
                puntaje = len(coincidencia[1]) * valorCoincidenciaUsuario["valorCoincidencia"]
                puntajes_por_inmueble.append({"idimueble": coincidencia[0], "puntaje": puntaje})
        puntaje_por_usuarios.append({"usuario": usuario, "puntajePorInmueble": puntajes_por_inmueble})
    return puntaje_por_usuarios

def obtener_datosLimpios(inmuebles,usuarios):
    datosLimpios = {}
    for item in usuarios:
        usuario = item[1]
        if usuario not in datosLimpios:
            datosLimpios[usuario] = {}
            for inmueble in inmuebles:
                id_inmueble = inmueble[0]
                datosLimpios[usuario][id_inmueble] = None
        else:
            print(f"El inmueble '{id_inmueble}' ya existe")

    return datosLimpios

def calcular_clasificaciones(datos, puntajes_por_usuarios, pesos,datosLimpios):
    calificaciones, clics, favoritos = [], [], []
    for item in datos:
        if item['calificacion']:
            calificaciones.append(item['calificacion'])
        if item['numeroDeClicks']:
            clics.append(item['numeroDeClicks'])
        if item['favorito']:
            favoritos.append(item['favorito'])

    promedio_calificaciones = sum(calificaciones) / len(calificaciones) if len(calificaciones)>0 else 1
    promedio_clics = sum(clics) / len(clics) if len(clics) else 0
    max_clics = max(clics) if len(clics) else 0
    promedio_favoritos = sum(favoritos) / len(favoritos) if len(favoritos) else 0

    for value in datos:
        id_inmueble = value['inmueble']
        usuario = value['usuario']
        calificacion = normalizacion(value['calificacion'], 5, 1) if value['calificacion'] else promedio_calificaciones
        favorito = int(value['favorito']) if value['favorito'] else promedio_favoritos
        clics = normalizacion(value['numeroDeClicks'], max_clics, 0) if value['numeroDeClicks'] and max_clics > 0 else promedio_clics

        preferencia = 0
        index_usuario = next((i for i, dic in enumerate(puntajes_por_usuarios) if dic["usuario"] == usuario), -1)
        if index_usuario != -1:
            puntajes_usuario = puntajes_por_usuarios[index_usuario]['puntajePorInmueble']
            index_inmueble = next((i for i, dic in enumerate(puntajes_usuario) if dic["idimueble"] == id_inmueble), -1)
            if index_inmueble != -1:
                preferencia = puntajes_usuario[index_inmueble]['puntaje']

        if id_inmueble and usuario:
            inmueble_por_usuario = InmuebleUsuarioNormalizado(
                inmueble=id_inmueble, usuario=usuario, calificacion=calificacion,
                favorito=favorito, clics=clics, puntaje_preferencia=preferencia, pesos=pesos
            )
            datosLimpios[usuario][id_inmueble] = inmueble_por_usuario.get_clasificacion()
    return datosLimpios

def guardar_datos(datosLimpios, nombre_archivo='datosLimpios.json'):
    with open(nombre_archivo, 'w') as archivo_json:
        json.dump(datosLimpios, archivo_json, indent=4)

def predecir_valoraciones(user, ratings_df, sim_df):
    user_ratings = ratings_df.loc[user]
    sim_scores = sim_df[user]

    sim_scores = sim_scores.drop(user)
    ratings_df = ratings_df.drop(user)

    weighted_sum = (ratings_df.T * sim_scores).sum(axis=1)
    sim_sum = sim_scores.sum()
    
    predicted_ratings = weighted_sum / sim_sum
    predicted_ratings = predicted_ratings[user_ratings.isna()]
    predicted_ratings = predicted_ratings[predicted_ratings > 0]

    return predicted_ratings.sort_values(ascending=False)

def generar_recomendaciones(usuario, datosLimpios):
    ratings_df = pd.DataFrame(datosLimpios).T
    cosine_sim = cosine_similarity(ratings_df.fillna(0))
    cosine_sim_df = pd.DataFrame(cosine_sim, index=ratings_df.index, columns=ratings_df.index)
    predicted_ratings = predecir_valoraciones(usuario, ratings_df, cosine_sim_df)
    print(predicted_ratings)
    return predicted_ratings.index.tolist()

def main(usuario):
    # Obtener datos de la API y la base de datos
    preferencias = get_datos_preferencias_por_usuario()
    columnas, resultados_inmuebles = consultar_base_de_datos('SELECT id FROM inmobiliaria_inmueble')
    columnas_user, resultados_usuarios = consultar_base_de_datos('SELECT id, username FROM inmobiliaria_usuario')
    inmuebles = get_datos_api(URL_API_INMUEBLES)
    datos_api = get_datos_api(URL_API)

    # Procesar datos
    intereses_por_usuario = procesar_intereses(preferencias)
    inmuebles_con_caracteristicas = procesar_inmuebles(inmuebles)
    coincidencias_todos_usuarios = calcular_coincidencias(intereses_por_usuario, inmuebles_con_caracteristicas)
    vCoincidenciasPorUsuario = valores_coincidencia_por_usuario(intereses_por_usuario, 10)
    puntajes_por_usuarios = puntajes_usuarios(coincidencias_todos_usuarios, vCoincidenciasPorUsuario)
    datosLimpios = obtener_datosLimpios(resultados_inmuebles,resultados_usuarios)
    datos = calcular_clasificaciones(datos_api, puntajes_por_usuarios, PESOS,datosLimpios)
    print(datos)
    # Guardar y generar recomendaciones
    guardar_datos(datos)
    recomendaciones = generar_recomendaciones(usuario=usuario, datosLimpios=datos)
    return recomendaciones
>>>>>>> d21868c5095cb7a889be5d7b191cd1d97edfabb0
