import csv, argparse, sys

uniquifier = ['', '重', '能', '重能']

parser = argparse.ArgumentParser()
parser.add_argument('priority_table')
parser.add_argument('mb_path', nargs='?')
args = parser.parse_args()

with open(args.priority_table, encoding='utf-8') as f:
    update_table = dict()
    for code, chars in csv.reader(f, delimiter='\t'):
        for i, char in enumerate(chars):
            update_table[char] = code + uniquifier[i]

if args.mb_path:
    with open(args.mb_path, encoding='utf-8') as f:
        mb = [(text,code) for text, code in csv.reader(f, delimiter='\t')]
else:
    mb = ((text,code) for text, code in
            csv.reader((line.strip() for line in sys.stdin), delimiter='\t'))

for text, code in mb:
    if text in update_table:
        code = update_table[text]

    print(f'{text}\t{code}')
