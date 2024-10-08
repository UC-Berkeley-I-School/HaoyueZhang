# scrabble.py
import itertools
from wordscore import score_word

def is_valid_word(word, rack):
    """Checks if a word can be formed using the letters in the given rack."""
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

def generate_wildcard_replacements(word, wildcard_count):
    """Generates words by replacing wildcards in the word with all letters A-Z."""
    if wildcard_count == 0:
        return [word]

    letters = 'abcdefghijklmnopqrstuvwxyz'
    replacements = set()
    wildcards = [i for i, char in enumerate(word) if char in ('*', '?')]

    for combination in itertools.product(letters, repeat=wildcard_count):
        new_word = list(word)
        for i, letter in zip(wildcards, combination):
            new_word[i] = letter
        replacements.add("".join(new_word))

    return replacements

def run_scrabble(rack):
    """Main function that processes the rack and returns valid words and their scores."""
    # Validate rack
    if not (2 <= len(rack) <= 7):
        return "Error: The rack must contain between 2 and 7 tiles."
    if any(char not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*?' for char in rack):
        return "Error: Invalid characters in the rack. Only A-Z, * and ? are allowed."
    if rack.count('*') > 1 or rack.count('?') > 1:
        return "Error: Only one '*' and one '?' wildcard are allowed."

    # Load valid words from file
    try:
        with open("sowpods.txt", "r") as infile:
            valid_words = {line.strip().upper() for line in infile}
    except FileNotFoundError:
        return "Error: The 'sowpods.txt' file is missing."

    # Process rack and generate words
    rack = rack.lower()
    letters = list(rack.replace('*', '').replace('?', ''))
    wildcard_count = rack.count('*') + rack.count('?')

    # Generate all possible combinations and words using the rack
    possible_words = set()
    for length in range(2, len(letters) + wildcard_count + 1):
        for combo in itertools.combinations(rack, length):
            for perm in itertools.permutations(combo):
                word = ''.join(perm)
                if wildcard_count > 0:
                    # Replace wildcards and generate new words
                    possible_words.update(generate_wildcard_replacements(word, wildcard_count))
                else:
                    possible_words.add(word)

    # Check against valid words and calculate scores
    valid_scores = []
    for word in possible_words:
        upper_word = word.upper()
        if upper_word in valid_words and is_valid_word(word, rack):
            score = score_word(word)
            valid_scores.append((score, upper_word))

    # Sort the words by score and alphabetically
    valid_scores.sort(key=lambda x: (-x[0], x[1]))

    return valid_scores, len(valid_scores)
