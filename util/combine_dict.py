import sys, csv

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} [码表一] [码表二] ……')
    quit()

mb = dict()
for file in sys.argv[1:]:
    with open(file, encoding='utf_8') as f:
        reader = csv.reader(f, delimiter='\t')
        mb.update({text:code for text, code in reader})

for text, code in mb.items():
    print(f'{text}\t{code}')
