from bd import obtener_conexion
import datetime as dt
from funciones_auxiliares import cipher_password, compare_password, create_session, delete_session
from flask import current_app

def login_usuario(username, passwordIn):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil, clave, numeroAccesosErroneo FROM usuarios WHERE estado='activo' and usuario = %s", (username,))
            usuario = cursor.fetchone()

            if usuario is None:
                ret = {"status": "ERROR", "mensaje": "Usuario/clave erroneo"}
                current_app.logger.info("Acceso usuario %s - USUARIO NO EXISTE", username)
                code = 200
            else:
                perfil = usuario[0]
                password = usuario[1]
                numAccesosErroneos = usuario[2]

                current_date = dt.date.today()
                hoy = current_date.strftime('%Y-%m-%d')

                if compare_password(password, passwordIn):
                    create_session(username, perfil)
                    ret = {"status": "OK", "perfil": perfil}
                    current_app.logger.info("Acceso usuario %s CORRECTO", username)
                    numAccesosErroneos = 0
                    estado = 'activo'
                else:
                    numAccesosErroneos = numAccesosErroneos + 1
                    if numAccesosErroneos > 2:
                        estado = "bloqueado"
                        current_app.logger.info("Usuario %s BLOQUEADO por %d intentos fallidos", username, numAccesosErroneos)
                    else:
                        estado = 'activo'
                    current_app.logger.info("Acceso usuario %s INCORRECTO", username)
                    ret = {"status": "ERROR", "mensaje": "Usuario/clave erroneo"}

                cursor.execute("UPDATE usuarios SET numeroAccesosErroneo=%s, fechaUltimoAcceso=%s, estado=%s WHERE usuario = %s", (numAccesosErroneos, hoy, estado, username))
                conexion.commit()
                code = 200
    except Exception as e:
        current_app.logger.error("Excepcion al validar al usuario: %s", str(e))
        ret = {"status": "ERROR"}
        code = 500
    finally:
        if conexion:
            conexion.close()
    return ret, code

def alta_usuario(username, password, perfil):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s", (username,))
            usuario = cursor.fetchone()
            if usuario is None:
                passwordC = cipher_password(password)
                cursor.execute("INSERT INTO usuarios(usuario, clave, perfil, estado, numeroAccesosErroneo) VALUES(%s, %s, %s, 'activo', 0)", (username, passwordC, perfil))
                if cursor.rowcount == 1:
                    conexion.commit()
                    current_app.logger.info("Nuevo usuario creado: %s", username)
                    ret = {"status": "OK"}
                    code = 200
                else:
                    ret = {"status": "ERROR"}
                    code = 500
            else:
                current_app.logger.info("Registro fallido - usuario ya existe: %s", username)
                ret = {"status": "ERROR", "mensaje": "Usuario ya existe"}
                code = 200
    except Exception as e:
        current_app.logger.error("Excepcion al registrar al usuario: %s", str(e))
        ret = {"status": "ERROR"}
        code = 500
    finally:
        if conexion:
            conexion.close()
    return ret, code

def logout():
    try:
        delete_session()
        ret = {"status": "OK"}
        code = 200
    except:
        ret = {"status": "ERROR"}
        code = 500
    return ret, code