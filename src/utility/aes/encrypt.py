import base64

from .initialize import SECRET_KEY, SALT, IV
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad


def encrypt(msg: str) -> str:
    key = PBKDF2(SECRET_KEY, SALT, dkLen=32, count=100000)
    cipher = AES.new(key, AES.MODE_CBC, iv=IV)
    padded_data = pad(msg.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(ciphertext).decode()
