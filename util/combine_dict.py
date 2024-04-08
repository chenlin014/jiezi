import sys, csv

mb = dict()
for file in sys.argv[1:]:
    with open(file, encoding='utf_8') as f:
        reader = csv.reader(f, delimiter='\t')
        mb.update({code:text for text, code in reader})

for code, text in mb.items():
    print(f'{text}\t{code}')
