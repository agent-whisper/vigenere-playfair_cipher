#!/usr/bin/python3
import copy
import json
import ordered_set
import random

class Vigenere:
  def __init__(self):
    # Decimal value of A in ASCII
    self.ASCII_OFFSET = 65
    
  def encipher(self, plaintext, key, isFullType=False, vigenere_square={}, plaintext_display_len=100):
    plaintext = plaintext.upper()
    key = key.upper()
    if len(plaintext) > plaintext_display_len:
      print('Plaintext:\n' + plaintext[:plaintext_display_len] + '...\n')
    else:
      print('Plaintext:\n' + plaintext + '\n')
    print('Key:\n' + key + '\n')
    ciphertext = ''
    key_idx = 0
    key_length = len(key)
    for plain_char in plaintext:
      key_char = key[key_idx % key_length]
      p = ord(plain_char)
      if not(p >= 65 and p <= 90):
        # character is not in range of A - Z
        ciphertext += plain_char
        continue
      else:
        if (isFullType):
          cipher_char = self._full_p_to_c(plain_char, key_char, vigenere_square)
        else:
          cipher_char = self._p_to_c(plain_char, key_char)
        # For checking encryption per character
        # print(plain_char, '+', key_char, '(', ord(key_char)-65, ')', '=>', cipher_char, '\n')
        ciphertext += cipher_char
        key_idx += 1
    return ciphertext

  def full_enchiper(self, plaintext, key, vigenere_square={}):
    ciphertext = 'failed to encipher'
    try:
      square = vigenere_square
      if len(vigenere_square) == 0:
        square = self._generate_random_square()
        self._write_square(square)
      ciphertext = self.encipher(plaintext, key, isFullType=True, vigenere_square=square)
    except KeyError as e:
      print('[vigenere.full_encipher] Error reading vigenere square: ' + str(e))
    return ciphertext

  def auto_key_enchiper(self, plaintext, key):
    auto_key = self._generate_auto_key(plaintext, key)
    return self.encipher(plaintext, auto_key)

  def running_key_enchiper(self, plaintext, key):
    return self.encipher(plaintext, key)

  def decipher(self, ciphertext, key, isFullType=False, vigenere_square={}, ciphertext_display_len=100):
    if len(ciphertext) > ciphertext_display_len:
      print('Ciphertext:\n' + ciphertext[:ciphertext_display_len] + '...\n')
    else:
      print('Ciphertext:\n' + ciphertext + '\n')
    if len(key) > 20:
      print('Key:\n' + key[:20] + '...\n')
    else:
      print('Key:\n' + key + '\n')
    plaintext = ''
    key_idx = 0
    key_length = len(key)
    
    for cipher_char in ciphertext:
      key_char = key[key_idx % key_length]
      c = ord(cipher_char)
      if not(c >= 65 and c <= 90):
        # character is not in range of A - Z
        plaintext += cipher_char
        continue
      else:
        if (isFullType):
          plain_char = self._full_c_to_p(cipher_char, key_char, vigenere_square)
        else:
          plain_char = self._c_to_p(cipher_char, key_char)
        # For checking encryption per character
        # print(cipher_char, '+', key_char, '(', ord(key_char)-65, ')', '=>', plain_char, '\n')
        plaintext += plain_char
        key_idx += 1
    return plaintext

  def full_decipher(self, ciphertext, key, square):
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = 'failed to decipher'
    try:
      plaintext = self.decipher(ciphertext, key, isFullType=True, vigenere_square=square)
    except FileExistsError as e:
      print('[vigenere.full_decipher] Error reading vigenere square: ', e)
    return plaintext

  def _generate_auto_key(self, plaintext, key):
    plain_idx = 0
    auto_key = key
    while len(auto_key) < len(plaintext):
      k = plaintext[plain_idx % len(plaintext)]
      if (ord(k) >= 65 and ord(k) < 91):
        auto_key += k
      plain_idx += 1
    return auto_key
    
  def _p_to_c(self, plain_char, key_char):
      p = ord(plain_char) - self.ASCII_OFFSET
      k = ord(key_char) - self.ASCII_OFFSET
      c = ((p + k) % 26) + self.ASCII_OFFSET
      return chr(c)

  def _c_to_p(self, cipher_char, key_char):
      c = ord(cipher_char) - self.ASCII_OFFSET
      k = ord(key_char) - self.ASCII_OFFSET
      p = ((c - k) % 26) + self.ASCII_OFFSET
      return chr(p)

  def _full_p_to_c(self, plain_char, key_char, vigenere_square):
      p = ord(plain_char) - self.ASCII_OFFSET
      c = vigenere_square[key_char][p]
      return c

  def _full_c_to_p(self, cipher_char, key_char, vigenere_square):
      p_idx = 0
      while (cipher_char != vigenere_square[key_char][p_idx]):
        p_idx += 1
      p = chr(p_idx + self.ASCII_OFFSET)
      return p

  def _generate_random_square(self):
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    cryptorand = random.SystemRandom()
    random_square = {}
    for i in range(65, 91):
      cryptorand.shuffle(alphabet)
      random_square[chr(i)] = copy.deepcopy(alphabet)
    return random_square

  def _write_square(self, vig_square):
    vig_square_save_dir = ''
    try:
      while vig_square_save_dir == '':
        vig_square_save_dir = input('Enter vigenere square json save directory:\n> ')
      with open(vig_square_save_dir, 'w+') as f:
        json.dump(vig_square, f)
    except IOError as e:
      print('[vigenere._write_square] Failed to write vigenere square json file: ' + str(e))
