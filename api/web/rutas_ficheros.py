from __future__ import print_function
from flask import request,Blueprint, jsonify, make_response, session
import controlador_ficheros
import os
from funciones_auxiliares import validar_session_normal

bp = Blueprint('ficheros', __name__)

def validar_csrf():
    token = session.get('csrf_token')
    csrf_header = request.headers.get('X-CSRFToken')
    if not token or token != csrf_header:
        return False
    return True

@bp.route ('/', methods=['POST'])
def upload():
    if not validar_session_normal():
        return make_response(jsonify({"status": "Forbidden"}), 403)
    if not validar_csrf():
        return make_response(jsonify({"status": "CSRF invalid"}), 403)
    try:
        if 'fichero' not in request.files:
            return make_response(jsonify({"status": "Bad parameters"}), 401)
        contenido = request.files['fichero']
        nombre = request.form.get("nombre")
        if not nombre or not isinstance(nombre, str) or len(nombre) > 255:
            return make_response(jsonify({"status": "Bad parameters"}), 401)
        if contenido.filename == '':
            return make_response(jsonify({"status": "Bad parameters"}), 401)
        respuesta,code = controlador_ficheros.guardar_fichero(nombre,contenido)
    except Exception as e:
        print(f"Error subiendo archivo: {e}", flush=True)
        respuesta={"status": "ERROR"}
        code=500
    return make_response(jsonify(respuesta), code)

@bp.route ('/<archivo>', methods=['GET'])
def ver(archivo):
    if not validar_session_normal():
        return make_response(jsonify({"status": "Forbidden"}), 403)
    if not isinstance(archivo, str) or '..' in archivo or '/' in archivo or '\\' in archivo:
        return make_response(jsonify({"status": "Bad parameters"}), 401)
    try:
        respuesta,code = controlador_ficheros.ver_fichero(archivo)
    except:
        respuesta= {"status": "ERROR"}
        code=500
    return make_response(jsonify(respuesta), code)
