import random
import string
import re


def create_hash_name(length):

    rand_str = ''.join([
        random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(length)
    ])

    return rand_str


def replace_word_in_file(file_path, original, replace_with):
    with open(file_path, 'r') as f:
        file = f.read()
        file = file.replace(original, replace_with)
    with open(file_path, 'w') as f:
        f.write(file)


def change_word_by_regex(file_path, regex, replace_with):
    with open(file_path, 'r') as f:
        file = f.read()
        found = regex.search(file)
    if found:
        replace_word_in_file(file_path, found[0], replace_with)
    else:
        raise ValueError(f"Matching String '{replace_with}' Not Found!")
