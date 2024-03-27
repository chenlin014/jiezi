import sys, json, csv
from gen_dict import trans_chord_map, ACTIONS

if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} <字根并击表> <键盘布局>')
    quit()

_, chord_map_path, keymap_path = sys.argv

with open(keymap_path) as f:
    km = json.loads(f.read())

with open(chord_map_path) as f:
    reader = csv.reader(f, delimiter='\t')
    chord_map = [(zg, ma) for zg, ma in reader]
chord_map = trans_chord_map(chord_map, km, ACTIONS)

print(f'''- "xform/{km['dup_key']}/重/"''')
print(f'''- "xform/{km['func_key']}/能/"''')
for zg, (lstroke, rstroke) in chord_map.items():
    print(f'''- "xform/`{lstroke}/{zg}/"''')
    print(f'''- "xform/{rstroke}`/{zg}/"''')
