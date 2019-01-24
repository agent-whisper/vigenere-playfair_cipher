#!/usr/bin/python3
import getopt
import json
import sys

cipher_type_list = {
  'vigenere' : 0,
  'full_vig' : 1,
  'auto_key_vig' : 2,
  'running_key_vig' : 3,
  'extended_vig' : 4,
  'playfair' : 5,
}

output_type_list = {
  'normal' : 0,
  'no_space' : 1,
  'grouped' : 2,
}

def parse_cli(argv):
  help_msg = 'python3 encrypt.py [-f <input file dir>] [-o <output file dir>] [-k <key file dir] [-d <cipher display>] '
  cipher_type = -1
  display_type = 0
  ifile = ''
  ofile = ''
  key_file = ''

  try:
    opts, args = getopt.getopt(argv, 'ht:d:f:o:k:', ['type=', 'display=', 'ifile=', 'ofile=', 'key='])
  except getopt.GetoptError:
    print(help_msg)
    sys.exit()

  for opt, arg in opts:
    if opt == '-h':
      print(help_msg)
    elif opt in ('-t', '--type'):
      try:
        cipher_type = cipher_type_list[arg]
      except KeyError:
        print('Cipher type does not exists')
        print('Available cipher type:')
        for t in cipher_type_list:
          print('- ' + t)
        sys.exit()
    elif opt in ('-d', '-display'):
      try:
        display_type = output_type_list[arg]
      except KeyError:
        print('Display type does not exists')
        print('Available display type (default = normal):')
        for t in output_type_list:
          print('- ' + t)
        sys.exit()
    elif opt in ('-f', '--ifile'):
      ifile = arg
    elif opt in ('-o', '--ofile'):
      ofile = arg
    elif opt in ('-k', '--key'):
      key_file = arg

  if cipher_type == -1:
    print('Please choose the cipher to be used')
    print('Available cipher type:')
    for t in cipher_type_list:
      print('- ' + t)
    sys.exit()

  elif (cipher_type == 3 and key_file == ''):
    print('running_key vigenere requires text-passage file as key ([-k <text passage file>])')
    sys.exit()

  return cipher_type, display_type, ifile, ofile, key_file

def read_input(ifile, text_type):
  if ifile == '':
    plaintext = input('Enter the %s:\n> ' % (text_type.upper()))
  else:
    try:
      with open(ifile, 'r') as f:
        plaintext = ''
        for line in f.readlines():
          plaintext += line
      print('%s file read successfully' % (text_type.upper()))
    except FileNotFoundError:
      print('[main] %s file not found' % (text_type.upper()))
  return plaintext.upper()

def read_input_bytes(ifile, text_type):
  plaintext = bytes('', 'utf-8')
  if ifile == '':
    plaintext = bytes(input('Enter your %s:\n> ' % (text_type.upper())), 'utf-8')
  else:
    try:
      with open(ifile, 'rb') as f:
        for line in f.readlines():
          plaintext += line
    except FileNotFoundError:
      print('[get_input_bytes] %s file not found' % (text_type.upper()))
      sys.exit()
    print('%s file was read successfully' % (text_type.upper()) + '\n')
  return plaintext

def read_key(key_file):
  if key_file == '':
    key = input('Enter the key:\n> ')
  else:
    try:
      with open(key_file, 'r') as f:
        key = ''
        for line in f.readlines():
          key += line
      print('Key file read successfully')
    except FileNotFoundError:
      print('[cipher_utils.read_key] Key file not found')
      sys.exit()
  final_key = filter_key(key.upper())
  return final_key

def read_vigenere_json(required=False):
  vigenere_data = {}
  json_dir = ''
  print('Enter vigenere square json file directory:')
  if required:
    while(json_dir == ''):
      json_dir = input('> ')  
  else:
    json_dir = input('(leave empty to generate random square) > ')  
  if (json_dir != ''):
    try:
      with open(json_dir, 'r') as f:
        data = json.load(f)
        vigenere_data = data.copy()
        print('Vigenere square file read successfully')
    except FileNotFoundError:
      print('[cipher_utils.read_vigenere_json] Vigenere square file not found')
      sys.exit()
  return vigenere_data

def save_output_bytes(data, output_dir):
  with open(output_dir, 'wb+') as f:
    f.write(data)

def save_output(text, output_dir):
  if output_dir != '':
    try:
      with open(output_dir, 'w+') as f:
        f.write(text)
      print('\nOutput saved to', output_dir)
      print()
    except FileNotFoundError:
      print('Current version does not support saving to not-existing directory')
      print()

def arrange_output(text, display_type):
  if display_type == 0:
    # as is
    return text
  elif display_type == 1:
    # without spaces
    return text.replace(' ', '')
  elif display_type == 2:
    # grouped in 5 characters
    group_count = 0
    arranged_text = ''
    for c in text:
      if c == ' ':
        continue
      arranged_text += c
      group_count = (group_count + 1) % 5
      if (group_count == 0):
        arranged_text += ' '
    return arranged_text

def filter_key(key):
  filtered_key = ''
  for k in key:
    if ord(k) < 65 or ord(k) > 90:
      if ord(k) >=97 and ord(k) <= 122:
        filtered_key += k.upper()
      else:
        continue
    else:
      filtered_key += k
  return filtered_key
