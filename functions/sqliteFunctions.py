import sqlite3

database = 'veterinaria.db'

def crear_mascotas():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especie TEXT NOT NULL,
            raza TEXT NOT NULL,
            edad INTEGER NOT NULL,
            color TEXT NOT NULL,
            fecha_registro DATE NOT NULL,
            veterinario_id INTEGER,
            FOREIGN KEY (veterinario_id) REFERENCES veterinarios (id)
        )
    ''')

    conexion.commit()
    conexion.close()

def agregar_mascota(nombre, especie, raza,  edad, color, fecha_registro, veterinario_id):
    # Crear la tabla si no existe
    crear_mascotas()

    # Insertar la nueva mascota
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO mascotas (nombre, especie, raza, edad, color, fecha_registro, veterinario_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, especie, raza, edad, color, fecha_registro, veterinario_id))

    conexion.commit()
    conexion.close()

def obtener_mascotas(veterinario_id):
    # Crear la tabla si no existe
    crear_mascotas()

    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('SELECT id, nombre FROM mascotas WHERE veterinario_id = ?', (veterinario_id,))
    mascotas = cursor.fetchall()
    conexion.close()
    return mascotas

def obtener_data_mascotas():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM mascotas')
    mascotas = cursor.fetchall()
    conexion.close()
    return mascotas

def crear_citas():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mascota INTEGER NOT NULL,
            id_veterinario INTEGER NOT NULL,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            motivo TEXT NOT NULL,
            FOREIGN KEY (id_mascota) REFERENCES mascotas (id),
            FOREIGN KEY (id_veterinario) REFERENCES veterinarios (id)
        )
    ''')

    conexion.commit()
    conexion.close()

def agregar_cita(id_mascota, id_veterinario, fecha, hora, motivo):
    # Crear la tabla si no existe
    crear_citas()

    # Insertar la nueva cita
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO citas (id_mascota, id_veterinario, fecha, hora, motivo)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_mascota, id_veterinario, fecha, hora, motivo))

    conexion.commit()
    conexion.close()

def obtener_citas():

    # Crear la tabla si no existe
    crear_citas()

    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('SELECT c.id, m.nombre, c.fecha, c.hora, c.motivo FROM citas c JOIN mascotas m ON c.id_mascota = m.id')
    citas = []
    for id, nombre, fecha, hora, motivo in cursor.fetchall():
        citas.append({
            "id": id,
            "title": f"{nombre} - {motivo}",
            "start": f"{fecha}T{hora}"
        })
    conexion.close()
    return citas

def crear_veterinarios():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veterinarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL  
            )
    ''')

    conexion.commit()
    conexion.close()

def agregar_veterinario(nombre, apellidos, especialidad, username, password):

    # Crear la tabla si no existe
    crear_veterinarios()

    # Insertar el nuevo veterinario
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO veterinarios (nombre, apellidos, especialidad, username, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, apellidos, especialidad, username, password))

    conexion.commit()
    conexion.close()

def checar_veterinario(username, password):
    # Obtener la lista de veterinarios
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM veterinarios WHERE username = ? AND password = ?', (username, password))
    veterinario = cursor.fetchone()
    conexion.close()
    
    if veterinario is None:
        # Si no se encuentra el veterinario, devolver None
        return None
    else:
        return veterinario    


# --- Operaciones graficos ---

def obtener_mascotas_por_especie():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('SELECT especie, COUNT(*) FROM mascotas GROUP BY especie')
    especies = cursor.fetchall()
    conexion.close()

    # Convertir a formato JSON
    data = []
    for especie, cantidad in especies:
        data.append({"especie": especie, "cantidad": cantidad})

    return data

def obtener_mascotas_por_raza():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('SELECT raza, COUNT(*) FROM mascotas GROUP BY raza')
    razas = cursor.fetchall()
    conexion.close()

    # Convertir a formato JSON
    data = []
    for raza, cantidad in razas:
        data.append({"raza": raza, "cantidad": cantidad})

    return data

def obtener_mascotas_por_mes():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT 
            CASE strftime('%m', fecha_registro)
                WHEN '01' THEN 'Enero'
                WHEN '02' THEN 'Febrero'
                WHEN '03' THEN 'Marzo'
                WHEN '04' THEN 'Abril'
                WHEN '05' THEN 'Mayo'
                WHEN '06' THEN 'Junio'
                WHEN '07' THEN 'Julio'
                WHEN '08' THEN 'Agosto'
                WHEN '09' THEN 'Septiembre'
                WHEN '10' THEN 'Octubre'
                WHEN '11' THEN 'Noviembre'
                WHEN '12' THEN 'Diciembre'
            END || ', ' || strftime('%Y', fecha_registro) AS mes,
            COUNT(*) 
        FROM mascotas 
        GROUP BY mes
        ORDER BY strftime('%Y', fecha_registro), strftime('%m', fecha_registro)
    ''')
    meses = cursor.fetchall()
    conexion.close()

    # Convertir a formato JSON
    data = []
    for mes, cantidad in meses:
        data.append({"mes": mes, "cantidad": cantidad})

    return data

def obtener_mascotas_por_edad():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('SELECT edad, COUNT(*) FROM mascotas GROUP BY edad')
    edades = cursor.fetchall()
    conexion.close()

    # Convertir a formato JSON
    data = []
    for edad, cantidad in edades:
        data.append({"edad": edad, "cantidad": cantidad})

    return data

def obtener_cita_por_dia():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT fecha, COUNT(*) 
        FROM citas 
        GROUP BY fecha
    ''')
    fechas = cursor.fetchall()
    conexion.close()

    # Convertir a formato JSON
    data = []
    for fecha, cantidad in fechas:
        data.append({"fecha": fecha, "cantidad": cantidad})

    return data

def obtener_cita_por_motivo():
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT motivo, COUNT(*) 
        FROM citas 
        GROUP BY motivo
    ''')
    motivos = cursor.fetchall()
    conexion.close()

    # Convertir a formato JSON
    data = []
    for motivo, cantidad in motivos:
        data.append({"motivo": motivo, "cantidad": cantidad})

    return data

# --- Operaciones CRUD para Mascotas ---

def eliminar_mascota(id):

    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM mascotas WHERE id = ?', (id,))
    conexion.commit()
    conexion.close()

def editar_mascota(id, data):
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('UPDATE mascotas SET nombre=?, especie=?, raza=?, edad=? WHERE id=?',
                   (data['nombre'], data['especie'], data['raza'], data['edad'], id))
    conexion.commit()
    conexion.close()


# --- Operaciones CRUD para Citas ---
def eliminar_cita(id):
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM citas WHERE id = ?', (id,))
    conexion.commit()
    conexion.close()

def obtener_cita(id):
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('SELECT id_mascota, fecha, hora, motivo FROM citas WHERE id = ?', (id,))
    cita = cursor.fetchone()
    conexion.close()
    return cita

def editar_cita(id, id_mascota, fecha, hora, motivo):
    conexion = sqlite3.connect(database)
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE citas
        SET id_mascota = ?, fecha = ?, hora = ?, motivo = ?
        WHERE id = ?
    ''', (id_mascota, fecha, hora, motivo, id))
    conexion.commit()
    conexion.close()

