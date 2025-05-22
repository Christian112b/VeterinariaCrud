import os

from functions.sqliteFunctions import *

from datetime import timedelta, date
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=15)

@app.before_request
def renovar_sesion():
    session.permanent = True    

@app.route('/')
def index():
    return render_template('login.html')

# ---- Login Functions ----

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
    return render_template('login.html', mensaje="Usuario registrado con éxito. Por favor, inicie sesión.", username=username, password=clave)


# --- Dates Functions ---
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

@app.route('/api/citas/<int:id>', methods=['DELETE'])
def remove_pet(id):
    eliminar_cita(id)
    return '', 204

@app.route('/api/getcitas/<int:id>', methods=['GET'])
def getCita(id):
    cita = obtener_cita(int(id))
    session['idCita'] = id
    return jsonify(cita)

@app.route('/edit_date', methods=['POST'])
def edit_date():
    
    id_cita = session['idCita']
    id_mascota = request.form['idMascota']
    id_vet = session['vetId']
    fecha = request.form['fechaCita']
    hora = request.form['horaCita']
    motivo = request.form['motivoCita']

    session.pop('idCita', None)

    editar_cita(id_cita, id_mascota, fecha, hora, motivo)

    return redirect(url_for('home'))

# --- Pets Functions ---

@app.route('/pets')
def pets():
    if 'username' not in session:
        return redirect(url_for('index'))

    # Obtener la lista de mascotas
    mascotas = obtener_data_mascotas()
    return render_template('petCrud.html', mascotas=mascotas)

@app.route('/register_pet', methods=['POST'])
def register_pet():
    nombre = request.form['nombreMascota']
    especie = request.form['especieMascota']
    raza = request.form['razaMascota']
    edad = request.form['edadMascota']
    color = request.form['colorMascota']
    fecha = date.today().strftime('%Y-%m-%d')

    agregar_mascota(nombre, especie, raza, edad, color, fecha, session['vetId'])

    return redirect(url_for('home'))

@app.route('/api/mascotas/<int:id>', methods=['DELETE'])
def delete_pet(id):
    eliminar_mascota(id)
    return '', 204

@app.route('/api/mascotas/<int:id>', methods=['PUT'])
def edit_pet(id):
    data = request.get_json()
    editar_mascota(id, data)
    return '', 204



@app.route('/home')
def home():

    if 'username' not in session:
        return redirect(url_for('index'))

    mascotas = obtener_mascotas(int(session['vetId']))  # Retornar una lista de tuplas (id, nombre)
    
    return render_template('home.html', mascotas=mascotas)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('vetId', None)
    return redirect(url_for('index'))


@app.route('/graphs')
def graphs():
    if 'username' not in session:
        return redirect(url_for('index'))

    # Obtener datos para las gráficas
    dictGraphs = {}


    #Mascotas por especie
    dictGraphs['graph1'] = obtener_mascotas_por_especie()

    #Mascotas por raza
    dictGraphs['graph2'] = obtener_mascotas_por_raza()

    #Mascotas registradas por mes
    dictGraphs['graph3'] = obtener_mascotas_por_mes()

    # Distribución de edades
    dictGraphs['graph4'] = obtener_mascotas_por_edad()

    #Citas por día
    dictGraphs['graph5'] = obtener_cita_por_dia()

    #Citas por motivo
    dictGraphs['graph6'] = obtener_cita_por_motivo()

    print(dictGraphs)

    return render_template('graphs.html', graphs=dictGraphs)



if __name__ == '__main__':
    app.run(debug=True)
