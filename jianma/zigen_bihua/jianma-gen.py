import csv, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('bh_table', help='字根笔画表')
parser.add_argument('bh_code', help='将笔画转换成编码')
parser.add_argument('mb_path', nargs='?', default=None, help='码表')
args = parser.parse_args()

with open(args.bh_code, encoding='utf_8') as f:
    bh_code = {bh: code for bh, code in
        csv.reader(f, delimiter='\t')}

with open(args.bh_table, encoding='utf_8') as f:
    zgbh = {zg: bh for zg, bh in
        csv.reader(f, delimiter='\t')}

if args.mb_path:
    with open(args.mb_path, encoding='utf_8') as f:
        reader = csv.reader(f, delimiter='\t')
        mb = [(char, code) for char, code in reader]
else:
    mb = [(char, code) for char, code in csv.reader(
            (line.strip() for line in sys.stdin), delimiter='\t')]

for char, code in mb:
    if len(code) <= 2:
        ncode = code
    elif len(code) == 3:
        c = bh_code[zgbh[code[1]]]
        ncode = code[0] + c[0] + code[-1] + (c[1] if len(c) > 1 else '')
    else:
        c = bh_code[zgbh[code[1]][0]+zgbh[code[-1]][0]]
        ncode = code[0] + c[0] + code[-1] + c[0]

    print(f'{char}\t{ncode}')
