import csv, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('subset')
parser.add_argument('source', nargs='?')
args = parser.parse_args()

if args.source:
    with open(args.source, encoding='utf_8') as f:
        mb = {zi:ma for zi, ma in csv.reader(f, delimiter='\t')}
else:
    mb = {zi:ma for zi, ma in
        csv.reader((line.strip() for line in sys.stdin), delimiter='\t')}

with open(args.subset, encoding='utf_8') as f:
    subset = set(f.read().splitlines())

for zi, ma in mb.items():
    if zi in subset:
        print(f'{zi}\t{ma}')
