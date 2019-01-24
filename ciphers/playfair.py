#!/usr/bin/python3
import ordered_set
import json

class Playfair:
  def __init__(self):
    self.ASCII_OFFSET = 65
  
  def encipher(self, plain_text, key, removed_char, placeholder_char):
    square_key = self._generate_square_key(key, removed_char)
    preprocessed_plain_text = self._preprocess_input_text(plain_text, removed_char)
    
    cursor = 0
    cipher_text = ''
    while cursor < len(preprocessed_plain_text):
      offset = 1
      new_char1 = ''
      new_char2 = ''
      try:
        char1 = preprocessed_plain_text[cursor]
        char2 = preprocessed_plain_text[cursor + offset]
        new_char1, new_char2, forward_steps = self._encrypt_character_pair(
            char1, char2, square_key, placeholder_char
        )
      except IndexError:
        # Final plain text has odd number of alphabets
        new_char1, new_char2, forward_steps = self._encrypt_character_pair(
            char1, placeholder_char, square_key, placeholder_char
        )
      cipher_text += new_char1 + new_char2
      cursor += (forward_steps + (offset - 1))
    return cipher_text

  def decipher(self, cipher_text, key, removed_char, placeholder_char):
    square_key = self._generate_square_key(key, removed_char)
    preprocessed_cipher_text = self._preprocess_input_text(cipher_text, removed_char)
    cursor = 0
    cipher_text = ''
    while cursor < len(preprocessed_cipher_text):
      offset = 1
      new_char1 = ''
      new_char2 = ''
      
      # cipher text should always has even number of character
      char1 = preprocessed_cipher_text[cursor]
      try:
          char2 = preprocessed_cipher_text[cursor + offset]
      except IndexError:
          print('decipher:')
          print(char1)
          print(cursor)
          print(offset)
      new_char1, new_char2, forward_steps = self._decrypt_character_pair(char1, char2, square_key, placeholder_char)
      
      cipher_text += new_char1 + new_char2
      cursor += (forward_steps + (offset - 1))
    cipher_text = self._decryption_postprocessing(cipher_text, placeholder_char)
    return cipher_text

  def _generate_square_key(self, key, removed_char):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet = alphabet.replace(removed_char, '')
    alphabet = ordered_set.OrderedSet(alphabet)

    preprocessed_key = key.upper()
    preprocessed_key = preprocessed_key.replace(removed_char, '')
    preprocessed_key = preprocessed_key.replace(' ', '')
    ordered_unique_key = ordered_set.OrderedSet(preprocessed_key)
    ordered_unique_key |= alphabet
    self._write_square_key(ordered_unique_key, 'playfair.json')
    return ordered_unique_key

  def _get_letter_index(self, character, ordered_unique_key):
    letter_idx = ordered_unique_key.index(character.upper())
    x = letter_idx % 5
    y = int(letter_idx / 5)
    return x, y
  
  def _preprocess_input_text(self, plain_text, removed_char):
    removed_char_idx = ord(removed_char) - self.ASCII_OFFSET
    replacement_char_idx = (removed_char_idx - 1) % 26
    replacement_char = chr(replacement_char_idx + self.ASCII_OFFSET)

    preprocessed_plain_text = plain_text.upper()
    preprocessed_plain_text = preprocessed_plain_text.replace(removed_char, replacement_char)
    preprocessed_plain_text = self._remove_foreign_characters(preprocessed_plain_text)
    return preprocessed_plain_text

  def _remove_foreign_characters(self, text):
    result = ''
    for c in text:
      c_idx = ord(c)
      if (c_idx < 65 or c_idx > 90):
        continue
      result += c
    return result

  def _encrypt_character_pair(self, char1, char2, square_key, placeholder_char):
    input_char1 = char1.upper()
    input_char2 = char2.upper()
    new_char1 = ''
    new_char2 = ''
    
    char1_x, char1_y = self._get_letter_index(input_char1, square_key)
    char2_x, char2_y = self._get_letter_index(input_char2, square_key)
    if input_char1 != input_char2:
      if char1_x == char2_x:
        # Kedua huruf sekolom
        new_char1_idx = char1_x + (char1_y + 1) % 5 * 5
        new_char2_idx = char2_x + (char2_y + 1) % 5 * 5
      elif char1_y == char2_y:
        # Kedua huruf sebaris
        new_char1_idx = (char1_x + 1) % 5 + char1_y * 5
        new_char2_idx = (char2_x + 1) % 5 + char2_y * 5
      else:
        new_char1_idx = (char2_x) + char1_y * 5
        new_char2_idx = (char1_x) + char2_y * 5
      new_char1 = square_key[new_char1_idx]
      new_char2 = square_key[new_char2_idx]
      return new_char1, new_char2, 2
    else:
      if input_char1 == placeholder_char:
        # Kedua huruf adalah placeholder (e.g. XX)
        new_char1_idx = (char1_x + 1) % 5 + (char1_y + 1) % 5 * 5
        new_char2_idx = (char2_x + 1) % 5 + (char2_y + 1) % 5 * 5
        new_char1 = square_key[new_char1_idx]
        new_char2 = square_key[new_char2_idx]
        return new_char1, new_char2, 2
      else:
        new_char1, new_char2, _ = self._encrypt_character_pair(char1, placeholder_char, square_key, placeholder_char)
        return new_char1, new_char2, 1
          
  def _decrypt_character_pair(self, char1, char2, square_key, placeholder_char):
    input_char1 = char1.upper()
    input_char2 = char2.upper()
    new_char1 = ''
    new_char2 = ''
    
    char1_x, char1_y = self._get_letter_index(input_char1, square_key)
    char2_x, char2_y = self._get_letter_index(input_char2, square_key)

    if input_char1 != input_char2:
      if char1_x == char2_x:
        # Kedua huruf sekolom
        new_char1_idx = char1_x + (char1_y - 1) % 5 * 5
        new_char2_idx = char2_x + (char2_y - 1) % 5 * 5
      elif char1_y == char2_y:
        # Kedua huruf sebaris
        new_char1_idx = (char1_x - 1) % 5 + char1_y * 5
        new_char2_idx = (char2_x - 1) % 5 + char2_y * 5
      else:
        new_char1_idx = (char2_x) + char1_y * 5
        new_char2_idx = (char1_x) + char2_y * 5
      new_char1 = square_key[new_char1_idx]
      new_char2 = square_key[new_char2_idx]
      return new_char1, new_char2, 2
    else:
      # Kedua huruf adalah placeholder (e.g. XX)
      new_char1_idx = (char1_x - 1) % 5 + (char1_y - 1) % 5 * 5
      new_char2_idx = (char2_x - 1) % 5 + (char2_y - 1) % 5 * 5
      new_char1 = square_key[new_char1_idx]
      new_char2 = square_key[new_char2_idx]
      return new_char1, new_char2, 2

  def _decryption_postprocessing(self, cipher_text, placeholder_char):
    cursor = 0
    postprocessed_plain_text = ''
    while cursor < len(cipher_text):
      current_char = cipher_text[cursor]
      try:
        next_char = cipher_text[cursor+1]
        if (current_char != placeholder_char and next_char == placeholder_char):
          # next_char maybe a placeholder
          try:
            next_next_char = cipher_text[cursor+2]
            if (current_char == next_next_char):
              # next_char is placeholder character
              postprocessed_plain_text += (current_char + '')
              cursor += 2
              continue
          except IndexError:
            # Check if placeholder at the end is a padding
            if (len(postprocessed_plain_text) % 2 == 1):
              postprocessed_plain_text += (current_char)
              cursor = len(cipher_text)
              continue
        elif (current_char == placeholder_char and next_char == placeholder_char):
          pass  
        postprocessed_plain_text += (current_char + next_char)
      except IndexError:
        # Check... something?
        pass
      cursor += 2
    return postprocessed_plain_text

  def _write_square_key(self, square_key, filename):
    sk = {}
    sk['square_key'] = list(square_key)
    with open(filename, 'w+') as f:
      json.dump(sk, f)