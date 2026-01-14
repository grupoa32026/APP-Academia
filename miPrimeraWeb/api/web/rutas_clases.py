from flask import request, Blueprint, jsonify
import controlador_clases
from funciones_auxiliares import Encoder

bp = Blueprint('clases', __name__)

@bp.route("/",methods=["GET"])
def clases():
    respuesta,code= controlador_clases.obtener_clases()
    return jsonify(respuesta), code
    
@bp.route("/<id>",methods=["GET"])
def clase_por_id(id):
    respuesta,code = controlador_clases.obtener_clase_por_id(id)
    return jsonify(respuesta), code

@bp.route("/",methods=["POST"])
def guardar_clase():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        clase_json = request.json
        idioma = clase_json["idioma"]
        nivel = clase_json["nivel"]
        precio=clase_json["precio"]
        foto=clase_json["foto"]
        respuesta,code=controlador_clases.insertar_clase(idioma, nivel,precio,foto)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/<int:id>", methods=["DELETE"])
def eliminar_clase(id):
    respuesta,code=controlador_clases.eliminar_clase(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_clase():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        clase_json = request.json
        id = clase_json["id"]
        idioma = clase_json["idioma"]
        nivel = clase_json["nivel"]
        precio=float(clase_json["precio"])
        foto=clase_json["foto"]
        respuesta,code=controlador_clases.actualizar_clase(id,idioma,nivel,precio,foto)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

