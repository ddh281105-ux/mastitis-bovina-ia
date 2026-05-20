from cryptography.fernet import Fernet

# =========================
# GENERAR CLAVE
# =========================

def generar_clave():

    clave = Fernet.generate_key()

    with open("clave.key", "wb") as archivo_clave:
        archivo_clave.write(clave)

# =========================
# CARGAR CLAVE
# =========================

def cargar_clave():

    return open("clave.key", "rb").read()

# =========================
# CIFRAR TEXTO
# =========================

def cifrar_dato(texto):

    clave = cargar_clave()

    f = Fernet(clave)

    texto_cifrado = f.encrypt(
        texto.encode()
    )

    return texto_cifrado

# =========================
# DESCIFRAR TEXTO
# =========================

def descifrar_dato(texto_cifrado):

    clave = cargar_clave()

    f = Fernet(clave)

    texto_descifrado = f.decrypt(
        texto_cifrado
    ).decode()

    return texto_descifrado
