import csv, sys

if len(sys.argv) < 3:
    print(f'{sys.argv[0]} <字根笔画表> <码表>')
    quit()

bh_name = {
    '一': '横',
    '丨': '竖',
    '丿': '撇',
    '丶': '捺',
    '㇕': '折',
    '㇆': '弯',
    '乚': '拐'
}

with open(sys.argv[1], encoding='utf_8') as f:
    reader = csv.reader(f, delimiter='\t')
    zgbh = {zg: ''.join(bh_name[h] for h in bh) for zg, bh in reader}

with open(sys.argv[2], encoding='utf_8') as f:
    reader = csv.reader(f, delimiter='\t')
    mb = [(char, code) for char, code in reader]

for char, code in mb:
    if len(code) <= 2:
        ncode = code
    elif len(code) == 3:
        bh = zgbh[code[1]]
        ncode = code[0] + bh[0] + code[-1] + (bh[1] if len(bh) > 1 else '')
    else:
        ncode = code[0] + zgbh[code[1]][0] + code[-1] + zgbh[code[-2]][0]

    print(f'{char}\t{ncode}')
