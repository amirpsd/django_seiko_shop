from string import digits, ascii_lowercase, ascii_uppercase
from random import choice


def code_generator(size, char=digits + ascii_lowercase + ascii_uppercase):
    return ''.join(choice(char) for _ in range(size))
