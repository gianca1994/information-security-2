from os import urandom

import blowfish
from passlib.utils import xor_bytes


class BlowFishCTR:
    def __init__(self, key_size):
        self.key = urandom(key_size)
        self.iv = urandom(8)
        self.bf = blowfish.Cipher(self.key)

    def encrypt(self, plaintext):
        return self._crypt(plaintext)

    def decrypt(self, ciphertext):
        return self._crypt(ciphertext).replace(b'\x00', b'')

    def _crypt(self, data):
        result = b''
        for i in range(0, len(data), 8):
            block = data[i:i + 8]
            if len(block) < 8:
                block += b'\x00' * (8 - len(block))
            iv = xor_bytes(self.iv, self.bf.encrypt_block(self.iv))
            result += xor_bytes(block, iv)
        return result
