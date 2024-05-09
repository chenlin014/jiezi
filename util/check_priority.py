def main() -> None:
    import argparse, csv, sys
    from find_duplicate import find_dup_code

    parser = argparse.ArgumentParser()
    parser.add_argument('priority_table')
    parser.add_argument('code_table')
    args = parser.parse_args()

    with open(args.priority_table, encoding='utf-8') as f:
        ptable = {code: chars for code, chars in
            csv.reader(f, delimiter='\t')}

    with open(args.code_table, encoding='utf-8') as f:
        mb = {text: code for text, code in
            csv.reader(f, delimiter='\t')}

    dup_code = find_dup_code(mb)

    missingTable = dict()
    extraTable = dict()
    for code, texts in dup_code.items():
        texts = set(texts)
        if not code in ptable:
            missingTable[code] = texts
            continue

        ptexts = set(ptable[code])
        missing = texts.difference(ptexts)
        if missing:
            missingTable[code] = missing

    for code, ptexts in ptable.items():
        ptexts = set(ptexts)
        if not code in dup_code:
            extraTable[code] = set(ptexts)
            continue

        texts = set(dup_code[code])
        extra = ptexts.difference(texts)
        if extra:
            extraTable[code] = extra

    if missingTable:
        print('缺少：')
        for code, texts in missingTable.items():
            print(f'{code}\t{",".join(texts)}')
        print()
    if extraTable:
        print('多余：')
        for code, texts in extraTable.items():
            print(f'{code}\t{",".join(texts)}')

if __name__ == '__main__':
    main()
