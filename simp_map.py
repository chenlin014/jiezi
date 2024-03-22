import re

def simp_code(code):
    suffix = re.search(r'[简正左下重能和喃韩]+', code)
    if suffix:
        suffix = suffix.group()
        code = code.replace(suffix, '')
    else:
        suffix = ''
    suffix = suffix.replace('左', '重').replace('下', '重')
    
    if len(code) <= 4:
        return code + suffix

    return code[:2] + code[-2:] + suffix


with open('zhengma.txt', encoding='utf-8') as f:
    mb = {text:simp_code(code) for text, code in (
        line.split('\t') for line in f.read().splitlines()
    )}

with open('xingzheng.txt', 'w', encoding='utf-8') as f:
    for text, code in mb.items():
        f.write(f'{text}\t{code}\n')
