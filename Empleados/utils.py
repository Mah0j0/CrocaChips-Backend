import bcrypt
def generar_usuario(nombre, apellido, carnet):
    usuario = f'{nombre[0].upper()}{apellido.split()[0]}{carnet[:2]}'
    return usuario

def generar_clave(nombre, apellido, carnet):
    clave = f'{nombre[0].upper()}{apellido[0].upper()}{carnet[-4:]}'
    return clave

def encriptar_clave(clave):
    clave_encriptada = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return clave_encriptada