import csv, sys

with open('stat/chang-digram-az', encoding='utf_8') as f:
    reader = csv.reader(f, delimiter='\t')
    digrams = {dg:chr(ord('가')+i) for i, (dg, _, _) in enumerate(reader) if i < int(sys.argv[1])}

with open(sys.argv[2], encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    mb = [(char, code) for char, code in reader]

for char, code in mb:
    if len(code) <= 2:
        ncode = code
    elif len(code) == 3:
        if code[1:] in digrams:
            ncode = code[0] + digrams[code[1:]]
        else:
            ncode = digrams.get(code[:2], code[0]) + code[-1]
    else:
        head = code[0]
        if code[:2] in digrams:
            head = digrams[code[:2]]
            head_len = 2

        tail = code[-1]
        if code[-2:] in digrams:
            tail = digrams[code[-2:]]

        ncode = head+tail

    print(f'{char}\t{ncode}')
