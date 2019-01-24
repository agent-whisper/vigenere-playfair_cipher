#!/usr/bin/python3
import sys

from cipher_utils import *
from ciphers.ext_vigenere import ExtendedVigenere
from ciphers.playfair import Playfair
from ciphers.vigenere import Vigenere

def main(argv):
  cipher_type, display_type, ifile, ofile, key_file = parse_cli(argv)
  print('\n == TUCIL 1 KRIPTOGRAFI ==\n')
  print(list(cipher_type_list.keys())[cipher_type].upper() + ' ENCRYPTION function selected\n')
  plaintext = ''
  key = ''
  ciphertext = ''
  if cipher_type == 4:
    plaintext = read_input_bytes(ifile, 'plaintext')
  else:
    plaintext = read_input(ifile, 'plaintext')
  key = read_key(key_file)
  
  if cipher_type == 0:
    print("\n==== USING VIGINERE CIPHER ====\n")
    ciphertext = Vigenere().encipher(plaintext, key)
  elif cipher_type == 1:
    print("\n==== USING FULL VIGINERE CIPHER ====\n")
    vigenere_square = read_vigenere_json()
    ciphertext = Vigenere().full_enchiper(plaintext, key, vigenere_square)
  elif cipher_type == 2:
    print("\n==== USING AUTO-KEY VIGINERE CIPHER ====\n")
    ciphertext = Vigenere().auto_key_enchiper(plaintext, key)
  elif cipher_type == 3:
    print("\n==== USING RUNNING-KEY VIGINERE CIPHER ====\n")
    ciphertext = Vigenere().encipher(plaintext, key)
  elif cipher_type == 4:
    print("\n==== USING EXTENDED VIGINERE CIPHER ====\n")
    ciphertext = ExtendedVigenere().encipher(plaintext, key)
  elif cipher_type == 5:
    print("\n==== USING PLAYFAIR CIPHER ====\n")
    print('NOTE: This cipher only has no_space (default) and grouped display-mode.\n')
    if display_type == 0:
      display_type = 1
    removed_char = input('Masukkan huruf yang dihilangkan > ').upper()
    placeholder_char = input('Masukkan huruf penyisip > ').upper()
    ciphertext = Playfair().encipher(plaintext, key, removed_char, placeholder_char)
  
  if hasattr(ciphertext, 'decode'):
    # ciphertext is in bytes
    while ofile == '':
      ofile = input('Enter encrytion result save directory:\n> ')
    save_output_bytes(ciphertext, ofile)
    print('Result saved to %s \n' % (ofile))
  else:
    # ciphertext is a string
    ciphertext = arrange_output(ciphertext, display_type)
    print('Encryption result:\n' + ciphertext + '\n')
    save_output(ciphertext, ofile)

if __name__ == '__main__':
  try:
    main(sys.argv[1:])
  except KeyboardInterrupt:
    print('\n\nExiting...\n\n')
    sys.exit()