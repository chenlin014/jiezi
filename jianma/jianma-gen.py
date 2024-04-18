import csv, sys, argparse

bh_name = {
    '一': '横',
    '丨': '竖',
    '丿': '撇',
    '丶': '捺',
    '㇕': '折',
    '㇆': '弯',
    '乚': '拐'
}

parser = argparse.ArgumentParser()
parser.add_argument('bh_table', help='字根笔画表')
parser.add_argument('mb_path', nargs='?', default=None,
    help='优先表：如何排序重码的字')
args = parser.parse_args()

with open(args.bh_table, encoding='utf_8') as f:
    reader = csv.reader(f, delimiter='\t')
    zgbh = {zg: ''.join(bh_name[h] for h in bh) for zg, bh in reader}

if args.mb_path:
    with open(sys.argv[2], encoding='utf_8') as f:
        reader = csv.reader(f, delimiter='\t')
        mb = [(char, code) for char, code in reader]
else:
    mb = [(char, code) for char, code in csv.reader(
            (line.strip() for line in sys.stdin), delimiter='\t')]

for char, code in mb:
    if len(code) <= 2:
        ncode = code
    elif len(code) == 3:
        bh = zgbh[code[1]]
        ncode = code[0] + bh[0] + code[-1] + (bh[1] if len(bh) > 1 else '')
    else:
        ncode = code[0] + zgbh[code[1]][0] + code[-1] + zgbh[code[-2]][0]

    print(f'{char}\t{ncode}')
