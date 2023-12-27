import re, csv

with open('xingzheng.txt', encoding='utf-8') as f:
    mb = dict()
    reader = csv.reader(f, delimiter='\t')

    for zi, ma in reader:
        mb[zi] = ma

# 正體
with open('xingzheng_zt.txt', 'w', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')
    for zi, ma in mb.items():
        xma = ma.replace('简和', '简').replace('正', '')
        xma = re.sub(r'[左下简和喃韩]', '重', xma)
        writer.writerow([zi, xma])

# 简体

# 日本
