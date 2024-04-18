import csv, re, sys

_, source, char_list = sys.argv

with open(source, encoding='utf_8') as f:
    r = csv.reader(f, delimiter='\t')
    mb = {zi:re.sub(r'[左下正简和喃韓]', '', ma) for zi, ma in r}

with open(char_list, encoding='utf_8') as f:
    chars = set(f.read().splitlines())

g = ((zi, ma) for zi, ma in mb.items() if zi in chars)
for zi, ma in g:
    print(f'{zi}\t{ma}')
