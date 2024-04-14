import csv, sys

bh_type = {
    '一': '一',
    '丨': '一',
    '丿': '丿',
    '丶': '丿',
    '㇕': '㇕',
    '㇆': '㇕',
    '乚': '㇕'
}

with open('test/zigen_bihua.tsv', encoding='utf_8') as f:
    reader = csv.reader(f, delimiter='\t')
    zgbh = {zg: ''.join(bh_type[h] for h in bh) for zg, bh in reader}

with open(sys.argv[1], encoding='utf_8') as f:
    reader = csv.reader(f, delimiter='\t')
    mb = [(char, code) for char, code in reader]

for char, code in mb:
    if len(code) <= 2:
        ncode = code
    else:
        ncode = code[0] + zgbh[code[1]] + code[-1]

    print(f'{char}\t{ncode}')
