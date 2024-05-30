import csv, sys

def gen_jianma(mb, methods, char_freq=dict()):
    used_texts = set()
    jm_table = dict()

    min_lens = []
    for method in methods:
        min_lens.append(
            max(i + 1 if i >= 0 else i * -1 for i in method)
        )

    for method, min_len in zip(methods, min_lens):
        for text, code in mb.items():
            if len(code) < min_len:
                continue

            ncode = ''.join(code[ind] for ind in method)
            if text in used_texts:
                continue
            if ncode in jm_table:
                if char_freq.get(text, 0) > char_freq.get(jm_table[ncode], 0):
                    used_texts.remove(jm_table[ncode])
                    jm_table[ncode] = text
                    used_texts.add(text)
            else:
                jm_table[ncode] = text
                used_texts.add(text)

        used_texts = set(jm_table.values())

    return jm_table

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('methods')
    parser.add_argument('table', nargs='?', default=None)
    parser.add_argument('--char-freq', default=None)
    args = parser.parse_args()

    methods = tuple(
                    tuple(map(int, method.split(',')))
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

    jm_table = gen_jianma(mb, methods, char_freq)

    for code, text in jm_table.items():
        print(f'{text}\t{code}')

if __name__ == '__main__':
    main()
