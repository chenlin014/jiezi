import json, csv, argparse

suffix_code = {
    '左':'<',
    '下':'v',
    '重':'y',
    '能':'z',
    '正':'Z',
    '简':'X',
    '韩':'Y',
    '和':'W',
    '喃':'V',
}

ACTIONS = {
    '0': (),
    '1': ('+1',),
    '2': ('0',),
    '3': ('+1', '0'),
    '4': ('-1',),
    '5': ('0', '-1'),
    'tk': {
        'a': (2,),
        'b': (1,),
        'c': (2, 1),
        'd': (0,),
        'e': (1, 0)
    }
}

def trans_chord_map(cm, km, acts):
    new_cm = dict()
    last_col = len(km['0']) - 1
    last_tk_col = len(km['thumb_keys']) - 1
    for zg, ma in cm:
        lstroke = ''.join(''.join(km[row][col] for row in acts[act])
            for col, act in enumerate(ma) if act in acts)
        rstroke = ''.join(''.join(km[row][last_col-col] for row in acts[act])
            for col, act in enumerate(ma) if act in acts)

        for act in ma:
            if act in acts['tk']:
                lstroke += ''.join(km['thumb_keys'][col] for col in acts['tk'][act])
                rstroke += ''.join(km['thumb_keys'][last_tk_col-col] for col in acts['tk'][act])

        new_cm[zg] = (lstroke, rstroke)

    return new_cm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('chordmap', help='字根并击表')
    parser.add_argument('keymap', help='键盘布局')
    parser.add_argument('mb_path', help='码表')
    parser.add_argument('-p', '--plover', action='store_true')
    args = parser.parse_args()

    with open(args.keymap) as f:
        km = json.loads(f.read())

    with open(args.chordmap) as f:
        reader = csv.reader(f, delimiter='\t')
        chord_map = [(zg, ma) for zg, ma in reader]
    chord_map = trans_chord_map(chord_map, km, ACTIONS)

    with open(args.mb_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        mb = {zi:ma for zi, ma in reader}
    codes = set(mb.values())

    suffix_code['重'] = km['dup_key']
    suffix_code['能'] = km['func_key']

    for zi, ma in mb.items():
        chords = []
        suffix = ''
        for i, code in enumerate(ma):
            if code == '空':
                continue

            if code in suffix_code:
                suffix += suffix_code[code]
                continue

            chords.append(chord_map[code][i%2])

        if ma + '简' in codes:
            suffix += suffix_code['正']
        if ma + '正' in codes:
            suffix += suffix_code['简']

        print(f'{zi}\t{"".join(chords)}')

if __name__ == '__main__':
    main()
