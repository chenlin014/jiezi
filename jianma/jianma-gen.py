import csv, sys

def gen_jianma(mb, methods, char_freq=dict()):
    texts = set()
    codes = set(mb.values())

    tables = list()
    for method in methods:
        table = dict()
        reverse_table = dict()
        for text, code in mb.items():
            ncode = ''.join(code[ind] for ind in method) if len(code) > len(method) else code
            if text in texts or ncode in codes:
                continue
            if ncode in reverse_table:
                if char_freq.get(text, 0) > char_freq.get(reverse_table[ncode], 0):
                    table.pop(reverse_table[ncode])
                    table[text] = ncode
                    reverse_table[ncode] = text
            else:
                table[text] = ncode
                reverse_table[ncode] = text

        texts = texts | set(table)
        codes = codes | set(table.values())

        tables.append(table)

    return tables

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('methods')
    parser.add_argument('table', nargs='?', default=None)
    parser.add_argument('--char-freq', default=None)
    args = parser.parse_args()

    methods = tuple(tuple(map(int, method.split(',')))
        for method in args.methods.split(':'))
    if args.table:
        with open(args.table, encoding='utf-8') as f:
            mb = {text:code for text, code in csv.reader(f, delimiter='\t')}
    else:
        mb = {text:code for text, code in
            csv.reader((line.strip() for line in sys.stdin), delimiter='\t')}

    if args.char_freq:
        with open(args.char_freq, encoding='utf-8') as f:
            char_freq = {char: float(freq) for char, freq in
                csv.reader(f, delimiter='\t')}
    else:
        char_freq = dict()

    tables = gen_jianma(mb, methods, char_freq)

    for table in tables:
        for text, code in table.items():
            print(f'{text}\t{code}')

if __name__ == '__main__':
    main()
