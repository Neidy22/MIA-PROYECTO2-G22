
import binascii

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class CipherA(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = key.encode()

    def encrypt(self, plain_text):
        plain_text = plain_text.encode()
        padded_text = pad(plain_text, self.bs)

        cipher = AES.new(self.key, AES.MODE_ECB)
        cipher_text = cipher.encrypt(padded_text)
        cipher_text = binascii.hexlify(cipher_text).decode('utf-8')

        return cipher_text

    def decrypt(self, cipher_text):

        cipher_text = binascii.unhexlify(cipher_text)
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_decrypted_text = cipher.decrypt(cipher_text)
        decrypted_text = unpad(padded_decrypted_text, self.bs).decode('utf-8')
        return str(decrypted_text)


#plain = 'miavacas123456'
#cip = CipherA(plain)
#encryptesU = cip.encrypt('contrasenia1486')
#print(f'Encriptado: {encryptesU}')
