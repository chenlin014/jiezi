import sys
sys.path.append('../rime')
from gen_dict import ACTIONS as acts

ON = '#'
OFF = '-'

ROWS = ['+1', '0']

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <并击表>')
    quit()

with open(sys.argv[1]) as f:
    chord_map = [(zg, chord) for zg, chord in (
        line.split('\t') for line in f.read().splitlines()
    )]

for zg, chord in chord_map:
    print(zg)
    for i in range(2):
        print(''.join(ON if ROWS[i] in acts[act] else OFF
            for act in chord if act in acts))

    for act in chord:
        if act in acts['tk']:
            print(''.join(ON if i in acts['tk'][act] else OFF
                for i in range(3)))
    print()
