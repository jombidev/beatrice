import base64

from .initialize import SECRET_KEY, SALT, IV
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad


def decrypt(msg: str) -> str:
    key = PBKDF2(SECRET_KEY, SALT, dkLen=32, count=100000)
    cipher = AES.new(key, AES.MODE_CBC, iv=IV)
    thingy = cipher.decrypt(base64.b64decode(msg))
    text = unpad(thingy, AES.block_size).decode()
    return text
