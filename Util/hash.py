import bcrypt
import binascii

def hashear_pass(password):
    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_password, salt)
    return hashed  

def comprobar_password(password_hasheada_bbdd, password_user):
    user_bytes = password_user.encode('utf-8')

    if isinstance(password_hasheada_bbdd, str) and password_hasheada_bbdd.startswith('\\x'):
        password_hasheada_bbdd = binascii.unhexlify(password_hasheada_bbdd[2:])

    resultado = bcrypt.checkpw(user_bytes, password_hasheada_bbdd)
    return resultado
