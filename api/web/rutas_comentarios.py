from __future__ import print_function
from flask import request,Blueprint, jsonify, g, make_response
import controlador_comentarios
from funciones_auxiliares import validar_session_normal

bp = Blueprint('comentarios', __name__)

@bp.route("/",methods=['POST'])
def agregar_comentario():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        comentario_json = g.cleaned_json
        if "usuario" in comentario_json and "descripcion" in comentario_json:
            usuario = comentario_json['usuario']
            descripcion = comentario_json['descripcion']
            if isinstance(usuario, str) and isinstance(descripcion, str) and len(usuario) < 50 and len(descripcion) < 1000:
                respuesta,code= controlador_comentarios.insertar_comentario(usuario,descripcion)
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

@bp.route("/",methods=['GET'])
def consultaComentarios():
    respuesta,code= controlador_comentarios.obtener_comentarios()
    return make_response(jsonify(respuesta), code)



