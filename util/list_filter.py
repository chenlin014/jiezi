import csv, re

with open('xingzheng.tsv', encoding='utf_8') as f:
    r = csv.reader(f, delimiter='\t')
    mb = {zi:re.sub(r'[左下正简和喃韓]', '', ma) for zi, ma in r}

with open('/home/chenlin/data/lang/zh/char_table/level-1.txt', encoding='utf_8') as f:
    chars = set(f.read().splitlines())

with open('xz.tsv', 'w', encoding='utf_8') as f:
    g = ((zi, ma) for zi, ma in mb.items() if zi in chars)
    for zi, ma in g:
        f.write(f'{zi}\t{ma}\n')
