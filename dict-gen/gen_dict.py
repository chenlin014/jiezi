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

def apply_keymap(code, system, acts=ACTIONS, onLeft=True):
    if code.startswith('<'):
        code = code[1:]
        onLeft = True
    if code.startswith('>'):
        code = code[1:]
        onLeft = False

    if onLeft:
        keys = set(''.join(''.join(system[row][col] for row in acts[act])
            for col, act in enumerate(code) if act in acts))
    else:
        keys = set(''.join(''.join(system[row][len(system['0'])-1-col] for row in acts[act])
            for col, act in enumerate(code) if act in acts))

    for act in code:
        if act in acts:
            continue

        if act in acts['tk']:
            if onLeft:
                keys = keys | set(''.join(system['thumb_keys'][col] for col in acts['tk'][act]))
            else:
                keys = keys | set(''.join(system['thumb_keys'][len(system['thumb_keys'])-1-col] for col in acts['tk'][act]))
        elif act in system['key_order']:
            keys.add(act)

    chord = list(keys)
    chord.sort(key=lambda k: system['key_order'][k])
    return ''.join(chord)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('system', help='并击系统')
    parser.add_argument('chordmap', help='字根并击表')
    parser.add_argument('mb_path', nargs='?', help='码表', default=None)
    args = parser.parse_args()

    with open(args.system) as f:
        system = json.loads(f.read())
    system['key_order'] = {key: i for i, key in enumerate(system['key_order'])}

    with open(args.chordmap) as f:
        reader = csv.reader(f, delimiter='\t')
        chord_map = {zg:(apply_keymap(ma, system, onLeft=True), apply_keymap(ma, system, onLeft=False)) for zg, ma in reader}

    if args.mb_path:
        with open(args.mb_path, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            mb = {zi:ma for zi, ma in reader}
    else:
        mb = {zi:ma for zi, ma in
            csv.reader((line.strip() for line in sys.stdin), delimiter='\t')}

    codes = set(mb.values())

    for zi, ma in mb.items():
        if re.match(r'\{.+\}', ma):
            chords = [apply_keymap(chord, system, onLeft=(i%2 == 0)) for i, chord in
                enumerate(ma[1:-1].split(','))]
            ma = ''
        else:
            chords = []

        for i, code in enumerate(ma.split(' ')):
            keys = set()
            for c in code:
                keys = keys | set(chord_map[c][i%2])

            chord = list(keys)
            chord.sort(key=lambda k: system['key_order'][k])
            chords.append(''.join(chord))

        strokes = [(lchord, rchord) for lchord, rchord in zip(chords[::2], chords[1::2])]

        if len(chords) % 2 == 1:
            strokes.append((chords[-1],))

        print(f'{zi}\t{" | ".join("<>".join(stroke) for stroke in strokes)}')

if __name__ == '__main__':
    main()
