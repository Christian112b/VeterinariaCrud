import os

from functions.sqliteFunctions import agregar_veterinario, checar_veterinario, agregar_mascota, obtener_mascotas, agregar_cita, obtener_citas

from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)
# app.permanent_session_lifetime = timedelta(minutes=15)

# @app.before_request
# def renovar_sesion():
#     session.permanent = True    

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/check_user', methods=['POST'])
def check_user():
    usuario = request.form['username']
    clave = request.form['password']

    veterinario = checar_veterinario(usuario, clave)

    if checar_veterinario(usuario, clave):
        session['vetId'] = veterinario[0]
        session['username'] = veterinario[1] + ' ' + veterinario[2]
        return redirect(url_for('home'))
    else:
        return render_template('login.html', mensaje="Credenciales inválidas")

@app.route('/register_user', methods=['POST'])
def register_user():

    nombre = request.form['nameVet']
    apellidos = request.form['apeVet']
    especialidad = request.form['especialidad']
    clave = request.form['password']

    parte_nombre = nombre[:3].capitalize()
    parte_apellido = apellidos[:3].capitalize()
    parte_especialidad = especialidad[:4].capitalize()

    # Generar el username    
    username = parte_nombre + parte_apellido + parte_especialidad

    agregar_veterinario(nombre, apellidos, especialidad, username, clave)

    # Redirigir a la página de inicio de sesión
    return render_template('login.html', mensaje="Usuario registrado con éxito. Por favor, inicie sesión.")

@app.route('/register_pet', methods=['POST'])
def register_pet():
    nombre = request.form['nombreMascota']
    especie = request.form['especieMascota']
    raza = request.form['razaMascota']
    edad = request.form['edadMascota']
    color = request.form['colorMascota']
    fecha = date.today().strftime('%Y-%m-%d')

    agregar_mascota(nombre, especie, raza, edad, color, fecha)

    return redirect(url_for('home'))

@app.route('/register_date', methods=['POST'])
def register_date():
    id_mascota = request.form['idMascota']
    vet_id = session['vetId']
    fecha = request.form['fechaCita']
    hora = request.form['horaCita']
    motivo = request.form['motivoCita']

    agregar_cita(id_mascota, vet_id, fecha, hora, motivo)

    return redirect(url_for('home'))

@app.route('/api/citas')
def api_citas():
    citas = obtener_citas()
    return jsonify(citas)

@app.route('/home')
def home():
    mascotas = obtener_mascotas()  # Retornar una lista de tuplas (id, nombre)
    
    return render_template('home.html', mascotas=mascotas)


if __name__ == '__main__':
    app.run(debug=True)
