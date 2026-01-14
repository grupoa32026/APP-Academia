from bd import obtener_conexion
import sys


def convertir_clase_a_json(clase):
    d = {}
    d['id'] = clase[0]
    d['idioma'] = clase[1]
    d['nivel'] = clase[2]
    d['precio'] = float(clase[3])
    d['foto'] = clase[4]
    return d

def insertar_clase(idioma, nivel, precio,foto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO clases(idioma, nivel, precio,foto) VALUES (%s, %s, %s,%s,%s)",
                       (idioma, nivel, precio,foto))
    conexion.commit()
    conexion.close()
    ret={"status": "OK" }
    code=200
    return ret,code

def obtener_clases():
    clasesjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, idioma, nivel, precio,foto FROM clases")
            clases = cursor.fetchall()
            if clases:
                for clase in clases:
                    clasesjson.append(convertir_clase_a_json(clase))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas las clases", flush=True)
        code=500
    return clasesjson,code

def obtener_clase_por_id(id):
    clasejson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, idioma, nivel, precio,foto FROM clases WHERE id =" + id)
            clase = cursor.fetchone()
            if clase is not None:
                clasejson = convertir_clase_a_json(clase)
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar una clase", flush=True)
        code=500
    return clasejson,code
def eliminar_clase(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM clases WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar una clase", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_clase(id, idioma, nivel, precio, foto):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE clases SET idioma = %s, nivel = %s, precio = %s, foto=%s WHERE id = %s",
                       (idioma, nivel, precio, foto,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al actualizar una clase", flush=True)
        ret = {"status": "Failure" }
        code=500
    return ret,code
