import csv, sys

def gen_luema(mb, methods):
    texts = set()
    codes = set(mb.values())

    tables = list()
    for method in methods:
        table = {code:text for code, text in
            ((code if len(code) <= len(method)
              else ''.join(code[ind] for ind in method),
             text)
            for text, code in mb.items())
            if not code in codes and not text in texts}

        texts = texts | set(table.values())
        codes = codes | set(table)

        tables.append(table)

    return tables

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('methods')
    parser.add_argument('table', nargs='?', default=None)
    args = parser.parse_args()

    methods = tuple(tuple(map(int, method.split(',')))
        for method in args.methods.split(':'))
    if args.table:
        with open(args.table, encoding='utf-8') as f:
            mb = {text:code for text, code in csv.reader(f, delimiter='\t')}
    else:
        mb = {text:code for text, code in
            csv.reader((line.strip() for line in sys.stdin), delimiter='\t')}

    tables = gen_luema(mb, methods)

    for i, table in enumerate(tables):
        print(f'{methods[i]}\t{len(table)}')
    print(f'{sum(len(table) for table in tables)}/{len(mb)}')

if __name__ == '__main__':
    main()
