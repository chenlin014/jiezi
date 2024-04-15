import csv, sys

if len(sys.argv) < 3:
    print(f'{sys.argv[0]} <字根笔画表> <码表>')

bh_type = {
    '一': '一',
    '丨': '丨',
    '丿': '丿',
    '丶': '丿',
    '㇕': '㇕',
    '㇆': '㇕',
    '乚': '㇕'
}

bh_pair = {
    '一': '横横',
    '丨': '竖横',
    '丿': '斜横',
    '㇕': '折横',
    '一一': '竖竖',
    '一丨': '横竖',
    '一丿': '横斜',
    '一㇕': '横折',
    '丨一': '竖横',
    '丨丨': '竖竖',
    '丨丿': '竖斜',
    '丨㇕': '竖折',
    '丿一': '斜横',
    '丿丨': '斜横',
    '丿丿': '斜斜',
    '丿㇕': '斜折',
    '㇕一': '折横',
    '㇕丨': '折竖',
    '㇕丿': '折斜',
    '㇕㇕': '折折'
}

with open(sys.argv[1], encoding='utf_8') as f:
    reader = csv.reader(f, delimiter='\t')
    zgbh = {zg: bh_pair[''.join(bh_type[h] for h in bh)] for zg, bh in reader}

with open(sys.argv[2], encoding='utf_8') as f:
    reader = csv.reader(f, delimiter='\t')
    mb = [(char, code) for char, code in reader]

for char, code in mb:
    if len(code) <= 2:
        ncode = code
    elif len(code) == 3:
        ncode = code[0] + zgbh[code[1]] + code[-1]
    else:
        ncode = code[0] + zgbh[code[1]][0] + zgbh[code[-2]][0] + code[-1]

    print(f'{char}\t{ncode}')
