from bd import obtener_conexion
import sys
import datetime as dt

def login_usuario(username,password):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s AND clave = %s", (username, password))
            usuario = cursor.fetchone()
            
            if usuario is None:
                ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
            else:
                ret = {"status": "OK" }
        code=200
    except Exception as e:
        print("Excepcion al validar al usuario", flush=True)
        print(str(e), flush=True)
        ret={"status":"ERROR"}
        code=500
    finally:
        if conexion:
            conexion.close()
    return ret,code

def alta_usuario(username,password,perfil):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s",(username,))
            usuario = cursor.fetchone()
            if usuario is None:
                cursor.execute("INSERT INTO usuarios(usuario,clave,perfil) VALUES(%s, %s, %s)", (username, password, perfil))
                if cursor.rowcount == 1:
                    conexion.commit()
                    ret={"status": "OK" }
                    code=200
                else:
                    ret={"status": "ERROR" }
                    code=500
            else:
                ret = {"status": "ERROR","mensaje":"Usuario ya existe" }
                code=200
    except Exception as e:
        print("Excepcion al registrar al usuario", flush=True)
        print(str(e), flush=True)
        ret={"status":"ERROR"}
        code=500
    finally:
        if conexion:
            conexion.close()
    return ret,code    

def logout():
    return {"status":"OK"},200

