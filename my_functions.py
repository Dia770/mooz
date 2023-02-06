import string
import random


def code_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# print(generator())
# print(generator(6, 'ABCDEF0123456789'))


def random_char(size=20, chars=string.ascii_lowercase + string.digits):
    size = random.randrange(10, 20)
    return ''.join(random.choice(chars) for _ in range(size))
