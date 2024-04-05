import sys

if len(sys.argv) < 3:
    print(f'{sys.argv[0]} <列表> <存至>')
    quit()

_, ls_file, save_at = sys.argv

with open(ls_file, encoding='utf_8') as f:
    ls = tuple(line.split()[0] for line in f.read().splitlines())
ls_len = len(ls)

with open(save_at, encoding='utf_8') as f:
    mb = {code:text for text, code in
        (line.split() for line in f.read().splitlines() if line)}
    finCount = len(mb)

if finCount >= len(ls):
    print('己完成')
    quit()

while finCount < ls_len:
    print(f'({finCount}/{ls_len}){ls[finCount]}')
    code = input()

    if code in mb:
        print(f'重码：{code}\t{mb[code]}\n')
        continue

    with open(save_at, 'a', encoding='utf_8') as f:
        f.write(f'{ls[finCount]}\t{code}\n')

    mb[code] = ls[finCount]
    finCount += 1
    print()

print('编码完成')
