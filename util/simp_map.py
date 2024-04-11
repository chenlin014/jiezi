import re

def simp_code(code, method):
    if len(code) <= len(method):
        return code
    return ''.join(code[ind] for ind in method)

def main():
    import sys
    if len(sys.argv) < 3:
        print(f'{sys.argv[0]} <码表> <取码法>')
        quit()

    _, mb_path, method = sys.argv
    method = tuple(int(ind) for ind in method.split(','))

    with open(mb_path, encoding='utf-8') as f:
        simp_map = ((text, simp_code(code, method)) for text, code in (
            line.split('\t') for line in f.read().splitlines()
        ))

    for text, code in simp_map:
        print(f'{text}\t{code}')

if __name__ == '__main__':
    main()
