import re, csv

with open('xingzheng.txt', encoding='utf-8') as f:
    mb = dict()
    reader = csv.reader(f, delimiter='\t')

    for zi, ma in reader:
        mb[zi] = ma
code_ls = set(mb.values())

# 正體
with open('xingzheng_zt.txt', 'w', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')
    for zi, ma in mb.items():
        if ma + '正' in code_ls:
            ma += '重'

        ma = ma.replace('简和', '简').replace('正', '')
        ma = re.sub(r'[左下简和喃韩]', '重', ma)

        writer.writerow([zi, ma])

# 简体

# 日本
