import csv, sys

with open(sys.argv[1], encoding='utf-8') as f:
    char_freq = {char: float(freq) for char, freq in
        csv.reader(f, delimiter='\t')}

for code, chars in csv.reader((line.strip() for line in sys.stdin), delimiter='\t'):
    chars = chars.split(',')
    chars.sort(reverse=True, key=lambda char: char_freq.get(char, 0))

    print(f'{code}\t{"".join(chars)}')
