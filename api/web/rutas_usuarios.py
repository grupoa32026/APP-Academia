from __future__ import print_function
from flask import request,Blueprint, jsonify, g, make_response, session
from flask_wtf.csrf import generate_csrf
from funciones_auxiliares import Encoder, validar_session_normal
import controlador_usuarios

bp = Blueprint('usuarios', __name__)

def validar_csrf():
    token = session.get('csrf_token')
    csrf_header = request.headers.get('X-CSRFToken')
    if not token or token != csrf_header:
        return False
    return True

@bp.route("/login",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = g.cleaned_json
        if "username" in login_json and "password" in login_json:
            username = login_json["username"]
            password = login_json["password"]
            if isinstance(username, str) and isinstance(password, str) and len(username) < 50 and len(password) < 50:
                respuesta,code= controlador_usuarios.login_usuario(username,password)
                if code == 200 and respuesta.get("status") == "OK":
                    csrf_token = generate_csrf()
                    session['csrf_token'] = csrf_token
                    respuesta["csrf_token"] = csrf_token
            else:
                respuesta={"status":"Bad parameters"}
                code=401
        else:
            respuesta={"status":"Bad parameters"}
            code=401
    else:
        respuesta={"status":"Bad request"}
        code=401
    return make_response(jsonify(respuesta), code)

@bp.route("/registro",methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = g.cleaned_json
        if "username" in login_json and "password" in login_json and "profile" in login_json:
            username = login_json["username"]
            password = login_json["password"]
            profile = login_json["profile"]
            if isinstance(username, str) and isinstance(password, str) and isinstance(profile, str) and len(username) < 50 and len(password) < 50 and len(profile) < 50:
                respuesta,code= controlador_usuarios.alta_usuario(username,password,profile)
            else:
                respuesta={"status":"Bad parameters"}
                code=401
        else:
            respuesta={"status":"Bad parameters"}
            code=401
    else:
        respuesta={"status":"Bad request"}
        code=401
    return make_response(jsonify(respuesta), code)


@bp.route("/logout",methods=['GET'])
def logout():
    if not validar_session_normal():
        return make_response(jsonify({"status": "Forbidden"}), 403)
    if not validar_csrf():
        return make_response(jsonify({"status": "CSRF invalid"}), 403)
    respuesta,code= controlador_usuarios.logout()
    return make_response(jsonify(respuesta), code)

