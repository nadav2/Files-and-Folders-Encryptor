import secrets
from encryptor import convert_to_source, convert_to_bytes
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from base64 import b64encode


def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, password):
    convert_to_bytes(file_name)
    salt_in_hex = secrets.token_hex(32)


    try:
        key = scrypt(password, salt_in_hex, 32, N=2 ** 14, r=8, p=1)
    except:
        try:
            password_bytes = password.encode("utf-8")
            password_base64 = b64encode(password_bytes)
            key = scrypt(str(password_base64), salt_in_hex, 32, N=2 ** 14, r=8, p=1)
        except:
            convert_to_source(file_name)
            password_bytes = password.encode("utf-8")
            password_base64 = b64encode(password_bytes)
            key = scrypt(str(password_base64), salt_in_hex, 32, N=2 ** 14, r=8, p=1)

    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)

    with open(file_name, 'wb') as fo:
        fo.write(enc)

    with open(file_name, 'a') as f:
        f.write(salt_in_hex)

def decrypt_file(file_name, password):
    salt = get_salt(file_name)

    if ver_file(file_name, password):
        try:
            key = scrypt(password, salt, 32, N=2 ** 14, r=8, p=1)
        except:
            password_bytes = password.encode("utf-8")
            password_base64 = b64encode(password_bytes)
            key = scrypt(str(password_base64), salt, 32, N=2 ** 14, r=8, p=1)

        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = decrypt(ciphertext[:-64], key)
        with open(file_name, 'wb') as fo:
            fo.write(dec)

        convert_to_source(file_name)
        return True
    else:
        return False

def ver_file(file_name, password):
    salt = get_salt(file_name)

    try:
        key = scrypt(password, salt, 32, N=16384, r=8, p=1)
    except:
        password_bytes = password.encode("utf-8")
        password_base64 = b64encode(password_bytes)
        key = scrypt(str(password_base64), salt, 32, N=2 ** 14, r=8, p=1)
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()

    dec = decrypt(ciphertext[:-64], key)
    dec_ver = str(dec[len(dec)-47:])
    dec_ver_final = dec_ver[2:-1]

    if dec_ver_final == "this is for verification only do not touch this":
        return True
    else:
        return False

def get_salt(file_name):
    with open(file_name, "rb") as f:
        data = f.read()
    salt = data[-64:]
    return salt.decode("utf-8")

