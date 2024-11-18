
import sys, os
from concurrent.futures import ProcessPoolExecutor
ABSDIR = os.path.dirname(os.path.realpath(__file__))

# # print ABSDIR
sys.path.append(os.path.join(ABSDIR,'..'))
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

from django.conf import settings


from vault.views import encrypt, decrypt
from libs.helpers import random_string
from django.contrib.auth.hashers import make_password


pin = '1337'

pin = make_password(pin)

def compare_hashes(p1):
    print(p1)
    if pin == make_password(str(p1)):
        print(p1)

# key2 = encrypt(1337)
# for i in range(9999):
#     print(i)
#     if pin == make_password(str(i)):
#         print(i)
#         break
#     # # print(i)
#     # print(make_password('1137'))
#     # if i == 1337:
#     #     print(key, decrypt(key))
#     #     print(key2, decrypt(key2))
#     #     print(encrypt(i), decrypt(encrypt(i)))
#     # if encrypt(str(i)) == key:
#     #     print(i)
#     #     break
if __name__ == '__main__':
    with ProcessPoolExecutor(4) as exe:
        results = exe.map(compare_hashes, range(9999))
# for i in range(9999):
#     compare_hashes(i)


# # SuperFastPython.com
# # example of a program that does not use all cpu cores
# import math
 
# # define a cpu-intensive task
# def task(arg):
#     return sum([math.sqrt(i) for i in range(1, arg)])
 
# # protect the entry point
# if __name__ == '__main__':
#     # report a message
#     print('Starting task...')
#     # perform calculations
#     results = [task(i) for i in range(1,50000)]
#     # report a message
#     print('Done.')
