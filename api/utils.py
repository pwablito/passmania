import string
import random
import hashlib


def generate_unique_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def hash_password(plaintext, salt):
    return hashlib.md5((salt + plaintext).encode()).hexdigest()
