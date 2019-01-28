#!/usr/bin/python3
import sys

from cipher_utils import *
from ciphers.ext_vigenere import ExtendedVigenere
from ciphers.playfair import Playfair
from ciphers.vigenere import Vigenere

def main(argv):
  cipher_type, display_type, ifile, ofile, key_file = parse_cli(argv)
  print(list(cipher_type_list.keys())[cipher_type].upper() + ' DECRYPTION function selected\n')
  ciphertext = ''
  key = ''
  plaintext = ''
  if cipher_type == 4:
    while ifile == '':
      ifile = input('Enter your cipher file directory:\n> ')
    ciphertext = read_input_bytes(ifile, 'ciphertext')
  else:
    ciphertext = read_input(ifile, 'ciphertext')
  key = read_key(key_file)
  print(cipher_type)
  if cipher_type == 0:
    print("\n==== USING VIGINERE CIPHER ====\n")
    plaintext = Vigenere().decipher(ciphertext, key)
  elif cipher_type == 1:
    print("\n==== USING FULL VIGINERE CIPHER ====\n")
    vigenere_square = read_vigenere_json(required=True)
    plaintext = Vigenere().full_decipher(ciphertext, key, vigenere_square)
  elif cipher_type == 2:
    print("\n==== USING AUTO-KEY VIGINERE CIPHER ====\n")
    plaintext = Vigenere().decipher(ciphertext, key)
  elif cipher_type == 3:
    print("\n==== USING RUNNING-KEY VIGINERE CIPHER ====\n")
    plaintext = Vigenere().decipher(ciphertext, key)
  elif cipher_type == 4:
    print("\n==== USING EXTENDED VIGINERE CIPHER ====\n")
    plaintext = ExtendedVigenere().decipher(ciphertext, key)
  elif cipher_type == 5:
    print("\n==== USING PLAYFAIR CIPHER ====\n")
    no_punc = True
    no_space = True
    if display_type == 0:
      no_punc = False
      no_space = False
    elif display_type == 1:
      no_punc = False
    removed_char = input('Masukkan huruf yang dihilangkan > ').upper()
    placeholder_char = input('Masukkan huruf penyisip > ').upper()
    plaintext = Playfair().decipher(ciphertext, key, removed_char, placeholder_char, no_punc=no_punc, no_space=no_space)
  
  if hasattr(plaintext, 'decode'):
    # ciphertext is in bytes
    while ofile == '':
      ofile = input('Enter decryption result save directory:\n> ')
    save_output_bytes(plaintext, ofile)
    print('Result saved to %s \n' % (ofile))
  else:
    # ciphertext is a string
    plaintext = arrange_output(plaintext, display_type)
    print('Decryption result:\n' + plaintext + '\n')
    save_output(plaintext, ofile)

if __name__ == '__main__':
  try:
    main(sys.argv[1:])
  except KeyboardInterrupt:
    print('\n\nExiting...\n\n')
    sys.exit()