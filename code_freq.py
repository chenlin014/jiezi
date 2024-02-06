import csv, sys

with open(sys.argv[1], encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    mb = {zi:ma for zi, ma in reader}
code_freq = {code:0 for code in set(''.join(mb.values()))}

if len(sys.argv) <= 2:
    for code in ''.join(mb.values()):
        code_freq[code] += 1
else:
    with open(sys.argv[2], encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        char_freq = [(char, int(freq)) for char, freq in reader]
    for char, freq in char_freq:
        if not char in mb:
            continue

        for code in mb[char]:
            code_freq[code] += freq

ranking = [(freq, code) for code, freq in code_freq.items()]
ranking.sort(reverse=True)

for freq, code in ranking:
    print(f'{code}\t{freq}')
