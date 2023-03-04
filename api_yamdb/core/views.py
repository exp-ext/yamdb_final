import secrets
import string


def get_key(length):
    """
    key Generator:
    length - key length
    """
    character_set = string.digits + string.ascii_letters
    return ''.join(secrets.choice(character_set) for _ in range(length))
