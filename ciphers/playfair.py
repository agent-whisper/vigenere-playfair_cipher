#!/usr/bin/python3
import ordered_set
import json

class Playfair:
  def __init__(self):
    self.ASCII_OFFSET = 65
  
  def encipher(self, plain_text, key, removed_char, placeholder_char, no_punc=True, no_space=True, plaintext_display_len=100):
    square_key = self._generate_square_key(key, removed_char)
    preprocessed_plain_text = self._preprocess_input_text(plain_text, removed_char, no_punc, no_space)
    if (len(preprocessed_plain_text) > plaintext_display_len):
      print('PLAINTEXT:\n%s...' % (preprocessed_plain_text[:plaintext_display_len]))
    else:
      print('PLAINTEXT:\n%s' % (preprocessed_plain_text))
    cursor = 0
    cipher_text = ''
    while cursor < len(preprocessed_plain_text):
      in_between_text = ''
      preceeding_text = ''
      offset = 1
      new_char1 = ''
      new_char2 = ''
      try:
        char1 = preprocessed_plain_text[cursor]
        while not(self.is_alphabet(char1)):
          preceeding_text += char1
          cursor += 1
          char1 = preprocessed_plain_text[cursor]
        char2 = preprocessed_plain_text[cursor + offset]
        while (not(self.is_alphabet(char2))):
          in_between_text += char2
          offset += 1
          char2 = preprocessed_plain_text[cursor + offset]
        new_char1, new_char2, forward_steps = self._encrypt_character_pair(
            char1, char2, square_key, placeholder_char
        )
      except IndexError:
        if self.is_alphabet(char1):
          # Final plain text has odd number of alphabets
          new_char1, new_char2, forward_steps = self._encrypt_character_pair(
              char1, placeholder_char, square_key, placeholder_char
          )
        else:
          pass
      cipher_text += preceeding_text + new_char1 + in_between_text + new_char2
      cursor += (forward_steps + (offset - 1))
    return cipher_text

  def decipher(self, cipher_text, key, removed_char, placeholder_char, no_punc=True, no_space=True):
    square_key = self._generate_square_key(key, removed_char)
    preprocessed_cipher_text = self._preprocess_input_text(cipher_text, removed_char, no_punc=no_punc, no_space=no_space)
    cursor = 0
    plaintext = ''
    while cursor < len(preprocessed_cipher_text):
      offset = 1
      new_char1 = ''
      new_char2 = ''
      in_between_text = ''
      preceeding_text = ''

      try:
        # cipher text should always has even number of character
        char1 = preprocessed_cipher_text[cursor]
        while not(self.is_alphabet(char1)):
            preceeding_text += char1
            cursor += 1
            char1 = preprocessed_cipher_text[cursor]
        char2 = preprocessed_cipher_text[cursor + offset]
        while (not(self.is_alphabet(char2))):
          in_between_text += char2
          offset += 1
          char2 = preprocessed_cipher_text[cursor + offset]
        
      except IndexError:
        print('decipher:')
        print(char1)
        print(cursor)
        print(offset)
      else:
        new_char1, new_char2, forward_steps = self._decrypt_character_pair(char1, char2, square_key, placeholder_char)
      
      plaintext += preceeding_text + new_char1 + in_between_text + new_char2
      cursor += (forward_steps + (offset - 1))
    plaintext = self._decryption_postprocessing(plaintext, placeholder_char)
    return plaintext

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
  
  def _preprocess_input_text(self, plain_text, removed_char, no_punc, no_space):
    removed_char_idx = ord(removed_char) - self.ASCII_OFFSET
    replacement_char_idx = (removed_char_idx - 1) % 26
    replacement_char = chr(replacement_char_idx + self.ASCII_OFFSET)

    preprocessed_plain_text = plain_text.upper()
    preprocessed_plain_text = preprocessed_plain_text.replace(removed_char, replacement_char)
    if not(no_punc and no_space):
      preprocessed_plain_text = self._remove_foreign_characters(preprocessed_plain_text, no_punc, no_space)
    return preprocessed_plain_text

  def _remove_foreign_characters(self, text, no_punc, no_space):
    result = ''
    for c in text:
      c_idx = ord(c)
      if (c_idx == 32) and no_space:
        continue
      elif (c_idx < 65 or c_idx > 90) and no_punc:
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
    output_text = ''
    while cursor < len(cipher_text):
      preceeding_text = ''
      in_between_text = ''
      potential_in_between_text = ''
      offset = 1
      offset_2 = 0
      current_char = cipher_text[cursor]
      while not(self.is_alphabet(current_char)):
        preceeding_text += current_char
        cursor += 1
        current_char = cipher_text[cursor]
      try:
        next_char = cipher_text[cursor + offset]
        while not(self.is_alphabet(next_char)):
          in_between_text += next_char
          offset += 1
          next_char = cipher_text[cursor + offset]

        if (current_char != placeholder_char and next_char == placeholder_char):
          # next_char maybe a placeholder
          try:
            offset_2 += 1
            next_next_char = cipher_text[cursor + offset + offset_2]
            while not(self.is_alphabet(next_next_char)):
              potential_in_between_text += next_next_char
              offset_2 += 1
              next_next_char = cipher_text[cursor + offset + offset_2]
            if (current_char == next_next_char):
              # next_char is placeholder character
              output_text += (preceeding_text + current_char + in_between_text + potential_in_between_text)
              cursor += (offset + offset_2)
              continue
          except IndexError:
            # Check if placeholder at the end is a padding
            output_text += (preceeding_text + current_char + in_between_text + potential_in_between_text)
            cursor = len(cipher_text)
            continue
        elif (current_char == placeholder_char and next_char == placeholder_char):
          pass  
        output_text += (preceeding_text + current_char + in_between_text + next_char + potential_in_between_text)
      except IndexError:
        # Check... something?
        output_text += preceeding_text + in_between_text
      cursor += (offset + offset_2 + 1)
    return output_text

  def _write_square_key(self, square_key, filename):
    sk = {}
    sk['square_key'] = list(square_key)
    with open(filename, 'w+') as f:
      json.dump(sk, f)

  def is_alphabet(self, ch):
    return (ord(ch) >= 65 and ord(ch) <= 90)