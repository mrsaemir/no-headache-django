import random
import string


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
