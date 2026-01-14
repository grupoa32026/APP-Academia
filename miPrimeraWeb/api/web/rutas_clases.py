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
        nombre = clase_json["nombre"]
        descripcion = clase_json["descripcion"]
        precio=clase_json["precio"]
        foto=clase_json["foto"]
        ingredientes=clase_json["ingredientes"]
        respuesta,code=controlador_clases.insertar_clase(nombre, descripcion,precio,foto,ingredientes)
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
        nombre = clase_json["nombre"]
        descripcion = clase_json["descripcion"]
        precio=float(clase_json["precio"])
        foto=clase_json["foto"]
        ingredientes=clase_json["ingredientes"]
        respuesta,code=controlador_clases.actualizar_clase(id,nombre,descripcion,precio,foto,ingredientes)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

