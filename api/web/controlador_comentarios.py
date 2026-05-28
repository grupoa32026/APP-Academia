from bd import obtener_conexion
from funciones_auxiliares import encode_output


def convertir_comentario_a_json(comentario):
    d = {}
    d['id'] = comentario[0]
    d['usuario'] = comentario[1]
    d['descripcion'] = comentario[2]
    return encode_output(d)

def insertar_comentario(usuario, descripcion):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO comentarios(usuario, descripcion) VALUES (%s, %s)", (usuario, descripcion))
            conexion.commit()
        ret={"status": "OK" }
        code=200
    except Exception as e:
        ret={"status": "ERROR" }
        print("Excepcion al insertar un comentario", flush=True)
        print(str(e), flush=True)
        code=500   
    finally:
        if conexion:
            conexion.close()
    return ret,code

def obtener_comentarios():
    comentariosjson=[]
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, usuario, descripcion FROM comentarios")
            comentarios = cursor.fetchall()
            if comentarios:
                for comentario in comentarios:
                    comentariosjson.append(convertir_comentario_a_json(comentario))
        code=200
    except Exception as e:
        print("Excepcion al consultar todas los comentarios", flush=True)
        print(str(e), flush=True)
        code=500
    finally:
        if conexion:
            conexion.close()
    return comentariosjson,code