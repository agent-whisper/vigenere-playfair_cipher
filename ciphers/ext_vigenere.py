#!/usr/bin/python3

class ExtendedVigenere:
  def __init__(self):
    pass
  
  def encipher(self, plain_bytes, key):
    print('\nKey:\n' + key + '\n')
    cipher_bytes = []
    key_idx = 0
    key_length = len(key)
    for pb in plain_bytes:
      key_char = key[key_idx % key_length]
      cipher_bytes.append(self._p_to_c(pb, key_char))
      key_idx += 1
    return bytes(cipher_bytes)

  def decipher(self, cipher_bytes, key):
    plain_bytes = []
    key_idx = 0
    key_length = len(key)
    for cb in cipher_bytes:
      key_char = key[key_idx % key_length]
      plain_bytes.append(self._c_to_p(cb, key_char))
      key_idx += 1
    return bytes(plain_bytes)

  def _p_to_c(self, plain_byte, key_char):
    c = ((plain_byte + ord(key_char)) % 256)
    return c

  def _c_to_p(self, cipher_byte, key_char):
    c = ((cipher_byte - ord(key_char)) % 256)
    return c