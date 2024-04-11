def find_dup_code(text2code):
    dup_code = dict()
    code2text = dict()

    for text, code in text2code.items():
        if not code in code2text:
            code2text[code] = text
            continue

        if code in dup_code:
            dup_code[code].append(text)
        else:
            dup_code[code] = [code2text[code], text]

    return dup_code

def main():
    import argparse, csv
    parser = argparse.ArgumentParser()
    parser.add_argument('table', help='码表文件')
    parser.add_argument('-pt', '--priority_table', default=None,
        help='优先表：如何排序重码的字')
    args = parser.parse_args()

    try:
        map_file = open(args.table, encoding='utf-8')
        mb = {text:code for text, code in (
            line.split('\t') for line in map_file.read().splitlines()
        )}
        map_file.close()
    except Exception as e:
        raise e

    if args.priority_table:
        with open(args.priority_table, encoding='utf_8') as f:
            reader = csv.reader(f, delimiter='\t')
            char_priority = {code:chars for code, chars in reader}
    else:
        char_priority = dict()

    dup_code = find_dup_code(mb)
    dup_code = {code: [char for char in chars if not char in char_priority.get(code, '')]
        for code, chars in dup_code.items()}
    dup_code = {code: chars for code, chars in dup_code.items() if len(chars) > 1}

    print(f'重码字数：{sum(len("".join(chars)) for chars in dup_code.values())}')
    for code, chars in dup_code.items():
        print(f'{code}\t{",".join(chars)}')

if __name__ == "__main__":
    main()
