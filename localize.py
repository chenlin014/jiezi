import re

with open('xingzheng.txt', encoding='utf-8') as f:
    lines = f.read().splitlines()
mb = {line[0]:line[1] for line in (
        line.split() for line in lines
    )}
codes = set(mb.values())

# 正體
with open('xingzheng_zt.txt', 'w', encoding='utf-8') as f:
    for zi, ma in mb.items():
        if ma + '正' in codes:
            xma = ma + '简'
        else:
            xma = ma
        if zi == '鸊':
            xma = '尸口辛鳥能'

        xma = xma.replace('简和', '重').replace('简', '重').replace('正', '')
        xma = re.sub(r'[和喃韩]', '重', xma)
        f.write(f'{zi}\t{xma}\n')

# 简体
with open('xingzheng_jt.txt', 'w', encoding='utf-8') as f:
    for zi, ma in mb.items():
        if ma + '简' in codes:
            xma = ma + '正'
        elif ma + '简和' in codes:
            xma = ma + '正'
        else:
            xma = ma
        if zi == '鸊':
            xma = '尸口辛鳥能'

        xma = xma.replace('简和', '').replace('简', '').replace('正', '重')
        xma = re.sub(r'[和喃韩]', '重', xma)
        f.write(f'{zi}\t{xma}\n')

# 日本
with open('xingzheng_jp.txt', 'w', encoding='utf-8') as f:
    for zi, ma in mb.items():
        if ma + '和' in codes:
            xma = ma + '重'
        elif ma + '简和' in codes:
            xma = ma + '重'
        elif ma + '正' in codes:
            xma = ma + '重'
        else:
            xma = ma
        if zi == '䴙':
            xma = '尸口辛鳥能'

        xma = xma.replace('简和', '').replace('和', '').replace('简', '重').replace('正', '')
        xma = re.sub(r'[喃韩]', '重', xma)
        f.write(f'{zi}\t{xma}\n')
