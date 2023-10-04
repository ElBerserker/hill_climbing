# TSP con hill climbing
import math
import random

from flask import Flask, render_template, request, jsonify
from operator import itemgetter

app = Flask(__name__)

coord = {}
pedidos = {}
almacen = None
max_carga = None

def distancia(coord1, coord2):
    lat1=coord1[0]
    lon1=coord1[1]
    lat2=coord2[0]
    lon2=coord2[1]
    return math.sqrt((lat1-lat2)**2+(lon1-lon2)**2)

def evalua_ruta(ruta):
    total=0
    for i in range(0,len(ruta)-1):
        ciudad1=ruta[i]
        ciudad2=ruta[i+1]
        total=total+distancia(coord[ciudad1], coord[ciudad2])
    ciudad1=ruta[i+1]
    ciudad2=ruta[0]
    total=total+distancia(coord[ciudad1], coord[ciudad2])

    return total

def hill_climbing():
    # crear ruta inicial aleatoria
    ruta=[]
    for ciudad in coord:
        ruta.append(ciudad)
    random.shuffle(ruta)

    mejora=True
    while mejora:
        mejora=False
        dist_actual=evalua_ruta(ruta)
        # evaluar vecinos
        for i in range(0,len(ruta)):
            if mejora:
                break
        for j in range(0,len(ruta)):
            if i!=j:
                ruta_tmp=ruta[:]
                ciudad_tmp=ruta_tmp[i]
                ruta_tmp[i]=ruta_tmp[j]
                ruta_tmp[j]=ciudad_tmp
                dist=evalua_ruta(ruta_tmp)
                if dist<dist_actual:
                    # se ha encontrado que vecino que mejora el resultado
                    mejora=True
                    ruta=ruta_tmp[:]
                    break
    return ruta

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/registrar_ciudad', methods=['POST'])
def registrar_ciudad():
    try:
        # Obtener los valores de latitud y longitud desde el formulario
        ciudad = str(request.form['ciudad'])
        latitud = float(request.form['latitud'])
        longitud = float(request.form['longitud'])

        #return render_template('resultado.html',nombre=nombre, latitud=latitud, longitud=longitud)
        coord[ciudad] = (latitud, longitud)
        return jsonify({"mensaje": f"Coordenadas de {ciudad} configuradas correctamente"})
    except ValueError:
        error_msg = "Por favor, ingresa todos los valores"
        return render_template('index.html', error_msg=error_msg)

@app.route('/mostrar_evaluacion', methods=['GET'])
def mostrar_evaluacion():
    try:
        if coord:
            # Llama a la función hill_climbing para obtener la ruta
            ruta_optima = hill_climbing()

            # Calcula la evaluación de la ruta óptima
            evaluacion = evalua_ruta(ruta_optima)

            return jsonify({"ruta_optima": ruta_optima, "evaluacion": evaluacion})

    except ValueError:
        error_msg = "Ocurrió un error al calcular la evaluación de la ruta."
        return jsonify({"error": error_msg})

if __name__ == '__main__':
    app.run(debug=True)
