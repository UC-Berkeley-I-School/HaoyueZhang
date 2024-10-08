# scrabble.py

import itertools
from wordscore import score_word

def is_valid_word(word, rack):

    rack_letters = list(rack)
    for letter in word:
        if letter in rack_letters:
            rack_letters.remove(letter)
        elif '*' in rack_letters:
            rack_letters.remove('*')
        elif '?' in rack_letters:
            rack_letters.remove('?')
        else:
            return False
    return True

def run_scrabble(rack):
    # Check for valid rack

    if not (2 <= len(rack) <= 7):
        return "Error: The rack must contain between 2 and 7 tiles."
    if any(char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*?' for char in rack):
        return "Error: Invalid characters in the rack. Only A-Z, * and ? are allowed."
    if rack.count('*') > 1 or rack.count('?') > 1:
        return "Error: Only one '*' and one '?' wildcard are allowed."、
    
    # Load from 'sowpods.txt'
    try:
        with open("sowpods.txt", "r") as infile:
            valid_words = [line.strip().upper() for line in infile]
    except FileNotFoundError:
        return "Error: The 'sowpods.txt' file is missing."

    rack = rack.lower()
    letters = list(rack.replace('*', '').replace('?', ''))
    wildcard_count = rack.count('*') + rack.count('?')

    possible_words = set()
    for length in range(2, len(letters) + wildcard_count + 1):
        for combo in itertools.combinations_with_replacement(rack, length):
            permutations = itertools.permutations(combo)
            for perm in permutations:
                word = ''.join(perm)
                possible_words.add(word)

    valid_scores = []
    for word in possible_words:
        upper_word = word.upper()
        if upper_word in valid_words and is_valid_word(word, rack):
            score = score_word(word)
            valid_scores.append((score, upper_word))

    valid_scores.sort(key=lambda x: (-x[0], x[1]))
    
    return valid_scores, len(valid_scores)
