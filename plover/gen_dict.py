import sys, json, csv, re

if len(sys.argv) != 4:
    print('Usage: gen_dict <char_mb> <zigen_mb> <system>')
    quit()
_, cmb_path, gmb_path, sys_path = sys.argv

with open(sys_path) as f:
    sys = json.loads(f.read())

with open(gmb_path) as f:
    reader = csv.reader(f, delimiter='\t')
    gmb = {zg:ma for zg, ma in reader}

with open(cmb_path) as f:
    reader = csv.reader(f, delimiter='\t')
    cmb = [(zi, ma) for zi, ma in reader]

print('{')
for char, code in cmb:
    suffix = re.search(r'[重能]+', code)
    if suffix:
        suffix = suffix.group()
        code = code.replace(suffix, '')
    else:
        suffix = ''

    strokes = ''
    for i, g in enumerate(code):
        stroke = ''
        for col, ins in enumerate(gmb[g]):
            if ins == '1':
                stroke += sys[i%2][col][0]
            elif ins == '2':
                stroke += sys[i%2][col][1]
            elif ins == '3':
                stroke += sys[i%2][col]

        if i == 0:
            strokes += stroke
        elif i % 2 == 0:
            strokes += '/'+stroke
        else:
            strokes += '-'+stroke

    mod = '-'
    if '重' in suffix:
        mod = sys[2][0] + mod
    if '能' in suffix:
        mod += sys[2][2]
    if not suffix and len(code) == 2:
        mod = '-' + sys[2][1]

    if mod != '-':
        slices = strokes.split('-')
        if len(slices) < 2:
            strokes = strokes.replace('-', mod)
        else:
            strokes = '-'.join(slices[:-1])+mod+slices[-1]
    
    print(f'"{strokes}": "{char}",')
print('}')
