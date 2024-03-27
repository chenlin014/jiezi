import sys, json, csv

ACTIONS = {
    '0': (),
    '1': ('+1',),
    '2': ('0',),
    '3': ('+1', '0'),
    '4': ('-1',),
    '5': ('0', '-1')
}

def trans_chord_map(cm, km, acts):
    new_cm = dict()
    for zg, ma in cm:
        last_col = len(km['0']) - 1
        lstroke = ''.join(''.join(km[row][col] for row in acts[act])
            for col, act in enumerate(ma))
        rstroke = ''.join(''.join(km[row][last_col-col] for row in acts[act])
            for col, act in enumerate(ma))

        new_cm[zg] = (lstroke, rstroke)

    return new_cm

def main():
    if len(sys.argv) < 4:
        print(f'Usage: {sys.argv[0]} <字根并击表> <键盘布局> <码表>')
        quit()
    _, chord_map_path, keymap_path, mb_path = sys.argv

    with open(keymap_path) as f:
        km = json.loads(f.read())

    with open(chord_map_path) as f:
        reader = csv.reader(f, delimiter='\t')
        chord_map = [(zg, ma) for zg, ma in reader]
    chord_map = trans_chord_map(chord_map, km, ACTIONS)

    with open(mb_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        mb = {zi:ma for zi, ma in reader}
    codes = set(mb.values())

    suffix_code = {
        '左':'D',
        '下':'V',
        '重':km['dup_key'],
        '能':km['func_key'],
        '正':'Z',
        '简':'J',
        '和':'W',
        '喃':'N',
        '韩':'H'
    }

    for zi, ma in mb.items():
        stroke = ''
        for i, code in enumerate(ma):
            if code == '空':
                continue

            if code in suffix_code:
                stroke += suffix_code[code]
                continue

            stroke += chord_map[code][i%2]

        if ma + '简' in codes:
            stroke += suffix_code['正']
        if ma + '正' in codes:
            stroke += suffix_code['简']

        print(f'{zi}\t{stroke}')

if __name__ == '__main__':
    main()
