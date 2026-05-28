from flask import request, Blueprint, jsonify, g, make_response, session
import controlador_clases
from funciones_auxiliares import Encoder, validar_session_normal

bp = Blueprint('clases', __name__)

def validar_csrf():
    token = session.get('csrf_token')
    csrf_header = request.headers.get('X-CSRFToken')
    if not token or token != csrf_header:
        return False
    return True

@bp.route("/",methods=["GET"])
def clases():
    if not validar_session_normal():
        return make_response(jsonify({"status": "Forbidden"}), 403)
    if not validar_csrf():
        return make_response(jsonify({"status": "CSRF invalid"}), 403)
    respuesta,code= controlador_clases.obtener_clases()
    return make_response(jsonify(respuesta), code)

@bp.route("/<id>",methods=["GET"])
def clase_por_id(id):
    if not validar_session_normal():
        return make_response(jsonify({"status": "Forbidden"}), 403)
    if not validar_csrf():
        return make_response(jsonify({"status": "CSRF invalid"}), 403)
    if not isinstance(id, str) or not id.isdigit():
        return make_response(jsonify({"status": "Bad parameters"}), 401)
    respuesta,code = controlador_clases.obtener_clase_por_id(id)
    return make_response(jsonify(respuesta), code)

@bp.route("/",methods=["POST"])
def guardar_clase():
    if not validar_session_normal():
        return make_response(jsonify({"status": "Forbidden"}), 403)
    if not validar_csrf():
        return make_response(jsonify({"status": "CSRF invalid"}), 403)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        clase_json = g.cleaned_json
        if "idioma" in clase_json and "nivel" in clase_json and "precio" in clase_json and "foto" in clase_json:
            idioma = clase_json["idioma"]
            nivel = clase_json["nivel"]
            precio = clase_json["precio"]
            foto = clase_json["foto"]
            if isinstance(idioma, str) and isinstance(nivel, str) and isinstance(foto, str) and len(idioma) < 100 and len(nivel) < 100 and len(foto) < 500:
                try:
                    precio_float = float(precio)
                    if precio_float < 0:
                        raise ValueError()
                except:
                    return make_response(jsonify({"status": "Bad parameters"}), 401)
                respuesta,code=controlador_clases.insertar_clase(idioma, nivel,precio_float,foto)
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

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_clase(id):
    if not validar_session_normal():
        return make_response(jsonify({"status": "Forbidden"}), 403)
    if not validar_csrf():
        return make_response(jsonify({"status": "CSRF invalid"}), 403)
    respuesta,code=controlador_clases.eliminar_clase(id)
    return make_response(jsonify(respuesta), code)

@bp.route("/", methods=["PUT"])
def actualizar_clase():
    if not validar_session_normal():
        return make_response(jsonify({"status": "Forbidden"}), 403)
    if not validar_csrf():
        return make_response(jsonify({"status": "CSRF invalid"}), 403)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        clase_json = g.cleaned_json
        if "id" in clase_json and "idioma" in clase_json and "nivel" in clase_json and "precio" in clase_json and "foto" in clase_json:
            id_val = clase_json["id"]
            idioma = clase_json["idioma"]
            nivel = clase_json["nivel"]
            precio = clase_json["precio"]
            foto = clase_json["foto"]
            if isinstance(id_val, (int, str)) and isinstance(idioma, str) and isinstance(nivel, str) and isinstance(foto, str) and len(idioma) < 100 and len(nivel) < 100 and len(foto) < 500:
                try:
                    precio_float = float(precio)
                    id_int = int(id_val)
                except:
                    return make_response(jsonify({"status": "Bad parameters"}), 401)
                respuesta,code=controlador_clases.actualizar_clase(id_int,idioma,nivel,precio_float,foto)
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

