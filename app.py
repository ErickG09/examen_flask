# Sistema web
# Librerías
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv['SQLALCHEMY_DATABASE_URI'] 

db = SQLAlchemy(app)

class Videogames(db.Model):
    # Definimos las columnas de la tabla para la Base de Datos
    id = db.Column(db.Integer, primary_key=True)  
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    desarrollador = db.Column(db.String(200), nullable=False)
    lanzamiento = db.Column(db.Integer, nullable=False)
    plataforma = db.Column(db.String(150), nullable=False)
    clasificacion = db.Column(db.String(100), nullable=False)
    imagen_url = db.Column(db.String(500), nullable=False)

    def GamesDb(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'desarrollador': self.desarrollador,
            'lanzamiento': self.lanzamiento,
            'plataforma': self.plataforma,
            'clasificacion': self.clasificacion,
            'imagen_url': self.imagen_url
        }
    
BASE_URL = '/api/'

# Ruta principal, solo mostrará un mensaje de bienvenida en una etiqueta h1
@app.route('/')
def home():
    return '<h1>Bienvenido a mi API de videojuegos</h1>'

#CRUD
# El siguiente paso es hacer el CRUD de la API
# Primero creamos el endpoint para crear videojuego usando la solicitud POST    

@app.route(BASE_URL + 'games', methods=['POST'])
def CrearVideojuego():
    if not request.json:
        abort(400, "Missing JSON body in request")
    if 'titulo' not in request.json:
        abort(400, "Error, missing 'titulo' in JSON data.")
    if 'descripcion' not in request.json:
        abort(400, "Error, missing 'descripcion' in JSON data.")
    if 'desarrollador' not in request.json:
        abort(400, "Error, missing 'desarrollador' in JSON data.")
    if 'lanzamiento' not in request.json:
        abort(400, "Error, missing 'lanzamiento' in JSON data.")
    if 'plataforma' not in request.json:
        abort(400, "Error, missing 'plataforma' in JSON data.")
    if 'clasificacion' not in request.json:
        abort(400, "Error, missing 'clasificacion' in JSON data.")
    if 'imagen_url' not in request.json:
        abort(400, "Error, missing 'imagen_url' in JSON data.")

    game = Videogames(titulo=request.json['titulo'], descripcion=request.json['descripcion'],
                      desarrollador=request.json['desarrollador'], lanzamiento=request.json['lanzamiento'],
                      plataforma=request.json['plataforma'], clasificacion=request.json['clasificacion'],
                      imagen_url=request.json['imagen_url'])
    db.session.add(game)  # Agrega la tarea a la BD
    db.session.commit()  # Guarda los cambios en la BD
    return jsonify({'Videojuegos': game.GamesDb}), 201 


# Endpoint para leer todos los videojuegos registrados con la solicitud GET
@app.route(BASE_URL + 'games', methods=['GET'])
def Leer_videojuegos():
    games = Videogames.query.all()  # Recupera todas las tareas de la BD
    return jsonify({'Videojuegos': [games.GamesDb() for game in games]}) 

# # LEER UNA TAREA ESPECÍFICA MEDIANTE EL ID CON LA SOLICITUD GET
# Endpoint para leer un registro de un videojuego mediante su id
@app.route(BASE_URL + 'games/<int:id>', methods=['GET'])
def Leer_videojuego(id):
    game = Videogames.query.get(id) # Obtenemos el registro 
    if game is None:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify({'Videojuegos': game.GamesDb()})

# # ACTUALIZAR EL ESTADO DE UNA TAREA CON LA SOLICITUD PUT
# Endpoint para actualiar el registro de algún videojuego mediante su id con la solicitud PUT
@app.route(BASE_URL + 'games/<int:id>', methods=['PUT'])
def Actualizar_juego(id):
    game = Videogames.query.get(id)
    if game is None:
        return jsonify({'error': 'Game not found'}), 404
    if not request.json:
        abort(400, "Missing JSON body in request")
    game = Videogames(titulo=request.json['titulo'], descripcion=request.json['descripcion'],
                      desarrollador=request.json['desarrollador'], lanzamiento=request.json['lanzamiento'],
                      plataforma=request.json['plataforma'], clasificacion=request.json['clasificacion'],
                      imagen_url=request.json['imagen_url'])
    db.session.add(game)  
    db.session.commit()  
    return jsonify({'Videojuegos': game.GamesDb()}), 201

# Endpoint para eliminar un registro de algún videojuego
@app.route(BASE_URL + 'games/<int:id>', methods=['DELETE'])
def delete_task(id):
    game = Videogames.query.get(id)
    if game is None:
        return jsonify({'error': 'Game not found'}), 404
    db.session.delete(game)  
    db.session.commit()  
    return jsonify({'result': True})  

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True) 