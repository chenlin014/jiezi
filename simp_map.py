import re

def simp_code(code, method):
    suffix = re.search(r'[简正左下重能和喃韩]+', code)
    if suffix:
        suffix = suffix.group()
        code = code.replace(suffix, '')
    else:
        suffix = ''
    suffix = suffix.replace('左', '重').replace('下', '重')
    
    if len(code) <= len(method):
        return code + suffix

    return ''.join(code[ind] for ind in method) + suffix

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
