import psycopg2
from psycopg2 import OperationalError

def conectar():
    try:
        conexion = psycopg2.connect(
            database="pruebatfg",
            user="postgres",
            password="redes",
            host="localhost"
        )
        return conexion
    except OperationalError as e:
        print("Error al conectar a la base de datos PruebaTFG:", e)
        return None
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

def iniciar_base_datos():
    master = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="redes",
        host="localhost"
    )
    master.autocommit = True
    curson1 = master.cursor()
    curson1.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        ("PruebaTFG",)
    )
    if not curson1.fetchone():
        curson1.execute("CREATE DATABASE PruebaTFG")
        print("Base de datos 'PruebaTFG' creada.")
    curson1.close()
    master.close()

    conexion = conectar()
    if conexion is None:
        raise RuntimeError("No se pudo conectar a PruebaTFG tras crearla")

    curson1 = conexion.cursor()
    curson1.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            pass VARCHAR(255) NOT NULL,
            imagen_perfil BYTEA
        )
    """)
    curson1.execute("""
        CREATE TABLE IF NOT EXISTS modulos_personalizados (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES usuarios(id),
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            contenido TEXT
        )
    """)
    curson1.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES usuarios(id),
            texto TEXT NOT NULL,
            fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            remitente VARCHAR(255) NOT NULL
        )
    """)
    conexion.commit()
    curson1.close()

    print("Tablas inicializadas en 'PruebaTFG'.")
    return conexion

def select_por_nombre(conexion,nombre): 
    try:
        cursor1 = conexion.cursor()
        cursor1.execute("SELECT * FROM usuarios WHERE nombre = %s", (nombre,))
        fila = cursor1.fetchone()
        cursor1.close()
        return fila
    except Exception as e:
        print("Error al conectar o consultar la base de datos:", e)

def select_user(conexion,nombre,password):
    try:
        cursor1 = conexion.cursor()
        cursor1.execute("SELECT * FROM usuarios WHERE nombre = %s AND pass = %s", (nombre,password))
        fila = cursor1.fetchone()
        cursor1.close()
        return fila
    except Exception as e:
        print("Error al conectar o consultar la base de datos:", e)

def insertar_usuarios(conexion, nombre, password):
    try:
        cursor1 = conexion.cursor()
        cursor1.execute("INSERT INTO usuarios (nombre,pass) VALUES (%s,%s)", (nombre,password))
        conexion.commit()
        cursor1.close()
    except Exception as e:
        print("Error al insertar usuarios:", e)

def eliminar_usuarios(conexion, email):
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id FROM usuarios WHERE nombre = %s",
            (email,)
        )
        fila = cursor.fetchone()
        if not fila:
            print(f"Usuario no encontrado: {email}")
            return False
        user_id = fila[0]

        cursor.execute("DELETE FROM modulos_personalizados WHERE user_id = %s",(user_id,))
        cursor.execute("DELETE FROM mensajes WHERE user_id = %s",(user_id,))
        cursor.execute("DELETE FROM usuarios WHERE id = %s",(user_id,))

        conexion.commit()
        cursor.close()
        return True

    except Exception as e:
        print("Error al eliminar usuarios:", e)

def modificar_nombre_usuario(conexion, email, nuevo_nombre):
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE usuarios SET nombre = %s WHERE nombre = %s",
            (nuevo_nombre, email)
        )
        conexion.commit()
        cursor.close()
        print(f"Nombre modificado para usuario id {email}")
    except Exception as e:
        print("Error al modificar el nombre del usuario:", e)

def modificar_password_usuario(conexion, email, nueva_password):
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE usuarios SET pass = %s WHERE nombre = %s",
            (nueva_password, email)
        )
        conexion.commit()
        cursor.close()
        print(f"Contraseña modificada para usuario id {email}")
    except Exception as e:
        print("Error al modificar la contraseña del usuario:", e)

def insertar_imagen(conexion, email, ruta_imagen):
    try:
        with open(ruta_imagen, 'rb') as archivo:
            datos_binarios = archivo.read()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE usuarios SET imagen_perfil = %s WHERE nombre = %s",
            (psycopg2.Binary(datos_binarios), email)
        )
        conexion.commit()
        cursor.close()
    except Exception as e:
        print("Error al guardar imagen:", e)

def select_imagen(conexion, email):
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen_perfil FROM usuarios WHERE nombre=%s",(email,))
    resultados = cursor.fetchone()
    cursor.close()
    if resultados and resultados[0]:
        return bytes(resultados[0])
    return None

def insertar_modulo(conexion, user_id, nombre, tipo, contenido):
    cursor = conexion.cursor()
    cursor.execute("""INSERT INTO modulos_personalizados (user_id, titulo, tipo, contenido ) VALUES (%s, %s, %s, %s)""", (user_id, nombre, tipo, contenido))
    conexion.commit()
    cursor.close()

def select_modulos_usuario(conexion, user_id):
    cursor = conexion.cursor()
    cursor.execute("""SELECT id, titulo, tipo, contenido FROM modulos_personalizados WHERE user_id = %s""", (user_id,))
    resultados = cursor.fetchall()
    cursor.close()
    return resultados

def select_modulos_titulo(conexion, user_id,titulo):
    cursor = conexion.cursor()
    cursor.execute("""SELECT id, user_id, titulo, tipo, contenido FROM modulos_personalizados WHERE user_id = %s AND titulo =%s""", (user_id, titulo,))
    resultados = cursor.fetchall()
    cursor.close()
    return resultados

def insertar_mensajes(conexion, user_id, mensajes, remitente):
    cursor= conexion.cursor()
    cursor.execute("""INSERT INTO mensajes (user_id, texto, remitente) VALUES (%s, %s, %s)""", (user_id, mensajes, remitente))
    conexion.commit()
    cursor.close()

def select_mensajes(conexion, user_id):
    cursor=conexion.cursor()
    cursor.execute("""SELECT id, user_id, texto, fecha, remitente FROM mensajes WHERE user_id = %s ORDER BY fecha""", (user_id,))
    resultados = cursor.fetchall()
    cursor.close()
    return resultados
