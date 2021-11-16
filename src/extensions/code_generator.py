from string import digits, ascii_lowercase, ascii_uppercase
from random import choice


def code_generator(
    size: int = 7, char: str = digits + ascii_lowercase + ascii_uppercase
) -> str:
    return "".join(choice(char) for _ in range(size))
