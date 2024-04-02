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

def find_nonpair(codes, enders):
    import re
    need_pair = (code for code in codes if re.search(rf'[{enders}]', code))

    return [code for code in need_pair if not code[:-1] in codes]

def main():
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path>")
        exit()

    try:
        map_file = open(sys.argv[1], encoding='utf-8')
        mb = {text:code for text, code in (
            line.split('\t') for line in map_file.read().splitlines()
        )}
        map_file.close()
    except Exception as e:
        raise e

    print(f'重码：{find_dup_code(mb)}')
    print(f'不成对：{find_nonpair(set(mb.values()), "正简左下重能和喃韓")}')

if __name__ == "__main__":
    main()
