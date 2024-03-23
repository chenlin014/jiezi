import sys

OFF_ON = '-#'
ACTS = {
    '0': (0, 0),
    '1': (1, 0),
    '2': (0, 1),
    '3': (1, 1)
}

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
        print(''.join(OFF_ON[ACTS[act][i]] for act in chord))
    print()
