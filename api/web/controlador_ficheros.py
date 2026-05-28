from __future__ import print_function
import os


def guardar_fichero(nombre,contenido):
    try:
        basepath = os.path.dirname(__file__)
        ruta_fichero = os.path.join(basepath, 'static/archivos', nombre)
        ruta_fichero = os.path.normpath(ruta_fichero)
        ruta_base = os.path.normpath(os.path.join(basepath, 'static/archivos'))
        if not ruta_fichero.startswith(ruta_base):
            return {"status": "ERROR"}, 403
        contenido.save(ruta_fichero)
        respuesta={"status": "OK"}
        code=200
    except Exception as e:
        print("Excepcion al guardar el ficheo", flush=True)
        print(str(e), flush=True)
        respuesta={"status": "ERROR"}
        code=500
    return respuesta, code

def ver_fichero(nombre):
    try:
        basepath = os.path.dirname(__file__)
        ruta_fichero = os.path.join(basepath, 'static/archivos', nombre)
        ruta_fichero = os.path.normpath(ruta_fichero)
        ruta_base = os.path.normpath(os.path.join(basepath, 'static/archivos'))
        if not ruta_fichero.startswith(ruta_base):
            return {"contenido": ""}, 403
        with open(ruta_fichero, 'r', encoding='utf-8', errors='ignore') as f:
            salida = f.read()
        respuesta={"contenido": salida}
        code=200
    except Exception as e:
        print("Excepcion al ver el frecuente", flush=True)
        print(str(e), flush=True)
        respuesta={"contenido":""}
        code=500
    return respuesta,code    


