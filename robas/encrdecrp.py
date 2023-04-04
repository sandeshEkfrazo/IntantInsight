import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from django.conf import settings

# settings.ENCRYPTED_ID

# data = 'I love Medium'

#FIX IV
# key = 'AAAAAAAAAAAAAAAA' #16 char for AES128


def encrypt(data,iv):
    data= pad(data.encode(),16)
    cipher = AES.new(settings.ENCRYPTED_ID.encode('utf-8'),AES.MODE_CBC,iv)
    return base64.b64encode(cipher.encrypt(data))

def decrypt(enc,iv):
    enc = base64.b64decode(enc)
    cipher = AES.new(settings.ENCRYPTED_ID.encode('utf-8'), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc),16)

