from flask import Flask, request, redirect, render_template, url_for
import requests

app = Flask(__name__)

API_BASE_URL = "https://examen-flask.onrender.com"  

@app.route('/gestion')
def gestion():
    # Recupera la lista de videojuegos
    response = requests.get(API_BASE_URL)
    videojuegos = response.json()['Videojuegos'] if response.status_code == 200 else []
    return render_template('templates\index.html', videojuegos=videojuegos)

@app.route('/crear', methods=['POST'])
def crear_videojuego():
    data = {
        'titulo': request.form['titulo'],
        'descripcion': request.form['descripcion'],
        'desarrollador': request.form['desarrollador'],
        'lanzamiento': request.form['lanzamiento'],
        'plataforma': request.form['plataforma'],
        'clasificacion': request.form['clasificacion'],
        'imagen_url': request.form['imagen_url'],
    }
    response = requests.post(API_BASE_URL, json=data)
    return redirect('/gestion')

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar_videojuego(id):
    data = {
        'titulo': request.form['titulo'],
        'descripcion': request.form['descripcion'],
        'desarrollador': request.form['desarrollador'],
        'lanzamiento': request.form['lanzamiento'],
        'plataforma': request.form['plataforma'],
        'clasificacion': request.form['clasificacion'],
        'imagen_url': request.form['imagen_url'],
    }
    response = requests.put(f"{API_BASE_URL}/{id}", json=data)
    return redirect('/gestion')

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_videojuego(id):
    response = requests.delete(f"{API_BASE_URL}/{id}")
    return redirect('/gestion')

if __name__ == '__main__':
    app.run(debug=True)