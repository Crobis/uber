import cv2
import pytesseract
import numpy as np
import os
import codecs

def wtf(path, content, kwargs = {}):
    mode = 'a' if os.path.exists(path) else 'w'
    f = codecs.open(path, mode, encoding='utf-8')
    f.write(content)
    f.close()

image_file = 'WowClassic_BcgNh3qFwn.png'

pytesseract.pytesseract.terreract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
base_path = 'c:\\Users\\uldsk\\Documents\\sharex\\Screenshots\\2024-05\\'
src = cv2.imread(base_path + image_file)
output_txt = pytesseract.image_to_string(src)

headers = [
    'Ace of Waves', # 3450
    '[Eight of Waves]', # 2000
    '[Five of Waves]', # 1600
    'Four of Waves', # 2300
    '[Seven of Waves]', # 1950
    '[Six of Waves]', # 2222
    'Three of Waves', # 2999
    'Two of Waves' # 1990
]

for header in headers:
    print('{0: <15}'.format(header), end='     ', flush=True)

print('')
with open('card_data.txt', 'r') as f:
    print(f.read())

total = 0
i = 0
for val in output_txt.split('\n'):


    val = val.replace('@','')
    val = val.split(' ')
    val = val[0]
    if val and i < 8:
        # print(val)
        i+=1

        total += int(val)

        print('{0: <15}'.format(val) , end='     ', flush=True)
        wtf('card_data.txt', '{0: <20}'.format(val))

# print(1/0)
print('')
print('total:', total)
wtf('card_data.txt', '\n')