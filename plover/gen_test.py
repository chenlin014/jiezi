import os, re

wd = os.path.dirname(__file__)

with open(wd+'/../zigen', encoding='utf-8') as f:
    zg = set(f.read().splitlines())

for i, g in enumerate(zg):
    if i == 0:
        code = '0000'
    else:
        code = ''
    num = i
    while num > 0:
        num, r = divmod(num, 4)
        code = str(r) + code

    if len(code) < 4:
        code = '0'*(4-len(code)) + code

    print(f'{g}\t{code}')
