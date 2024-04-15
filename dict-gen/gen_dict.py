import json, csv, argparse, sys, re

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

def apply_keymap(code, km, acts=ACTIONS, onLeft=True):
    if onLeft:
        chord = ''.join(''.join(km[row][col] for row in acts[act])
            for col, act in enumerate(code) if act in acts)
    else:
        chord = ''.join(''.join(km[row][len(km['0'])-1-col] for row in acts[act])
            for col, act in enumerate(code) if act in acts)

    for act in code:
        if act in acts['tk']:
            if onLeft:
                chord += ''.join(km['thumb_keys'][col] for col in acts['tk'][act])
            else:
                chord += ''.join(km['thumb_keys'][len(km['thumb_keys'])-1-col] for col in acts['tk'][act])

    return chord

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('chordmap', help='字根并击表')
    parser.add_argument('keymap', help='键盘布局')
    parser.add_argument('-mp', '--mb_path', help='码表', default=None)
    parser.add_argument('-pt', '--priority_table', default=None)
    args = parser.parse_args()

    with open(args.keymap) as f:
        km = json.loads(f.read())

    uniquifier = ['', km["dup_key"], km["func_key"], km["dup_key"]+km["func_key"]]

    with open(args.chordmap) as f:
        reader = csv.reader(f, delimiter='\t')
        chord_map = {zg:(apply_keymap(ma, km, onLeft=True), apply_keymap(ma, km, onLeft=False)) for zg, ma in reader}

    if args.mb_path:
        with open(args.mb_path, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            mb = {zi:ma for zi, ma in reader}
    else:
        mb = {zi:ma for zi, ma in
            csv.reader((line.strip() for line in sys.stdin), delimiter='\t')}

    codes = set(mb.values())

    if args.priority_table:
        with open(args.priority_table, encoding='utf_8') as f:
            reader = csv.reader(f, delimiter='\t')
            char_priority = {code: chars for code, chars in reader}
    else:
        char_priority = dict()

    for zi, ma in mb.items():
        if re.match(r'\{.+\}', ma):
            chords = [apply_keymap(chord, km, onLeft=(i%2 == 0)) for i, chord in
                enumerate(ma[1:-1].split(','))]
            ma = ''
        else:
            chords = []

        for i, code in enumerate(ma.split(' ')):
            chord = ''
            for c in code:
                if c == '重':
                    chord += km['dup_key']
                elif c == '能':
                    chord += km['func_key']
                else:
                    chord += chord_map[c][i%2]
            chords.append(chord)

        if ma in char_priority:
            try:
                ind = char_priority[ma].index(zi)
                chords[-1] += uniquifier[ind]
            except Exception as e:
                print(f'\n{zi}\t{ma}')
                raise e

        strokes = [(lchord, rchord) for lchord, rchord in zip(chords[::2], chords[1::2])]

        if len(chords) % 2 == 1:
            strokes.append((chords[-1],))

        print(f'{zi}\t{" | ".join("<>".join(stroke) for stroke in strokes)}')

if __name__ == '__main__':
    main()
