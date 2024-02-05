import csv, sys

with open(sys.argv[1], encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')

    codes = ''.join([row[1] for row in reader])

code_freq = {code:0 for code in set(codes)}
for code in codes:
    code_freq[code] += 1

ranking = [(freq, code) for code, freq in code_freq.items()]
ranking.sort(reverse=True)

for freq, code in ranking:
    print(f'{code}\t{freq}')
