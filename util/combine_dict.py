import sys, csv

mb = dict()
for file in sys.argv[1:]:
    with open(file, encoding='utf_8') as f:
        reader = csv.reader(f, delimiter='\t')
        mb.update({text:code for text, code in reader})

for text, code in mb.items():
    print(f'{text}\t{code}')
