import sys, json, csv, re

if len(sys.argv) < 3:
    print('Usage: gen_dict <zigen_mb> <keymap> [char_mb]')
    quit()
_, gmb_path, km_path = sys.argv[:3]
if len(sys.argv) >= 4:
    mb_path = sys.argv[3]
else:
    mb_path = False

with open(km_path) as f:
    km = json.loads(f.read())

with open(gmb_path) as f:
    reader = csv.reader(f, delimiter='\t')
    gmb = [(zg, ma) for zg, ma in reader]

lgmb = dict()
rgmb = dict()
for zg, ma in gmb:
    lstroke = ''
    rstroke = ''

    for col, act in enumerate(ma):
        if act == '0':
            continue
        elif act == '1':
            lstroke += km[0][col]
            rstroke += km[0][7-col]
        elif act == '2':
            lstroke += km[1][col]
            rstroke += km[1][7-col]
        else:
            lstroke += km[0][col] + km[1][col]
            rstroke += km[0][7-col] + km[1][7-col]

    lgmb[zg] = lstroke
    rgmb[zg] = rstroke

if not mb_path:
    print(f'''- "xform/重/{km[2][2]}/"''')
    print(f'''- "xform/能/{km[2][3]}/"''')
    for zg in lgmb:
        print(f'''- "xform/`{zg}/{lgmb[zg]}/"''')
        print(f'''- "xform/{zg}`/{rgmb[zg]}/"''')
    
    quit()

with open(mb_path, encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    mb = {zi:ma for zi, ma in reader}
codes = set(mb.values())

suffix_code = {
    '左':'D',
    '下':'V',
    '重':km[2][2],
    '能':km[2][3],
    '正':'Z',
    '简':'J',
    '和':'W',
    '喃':'N',
    '韩':'H'
}

for zi, zma in mb.items():
    stroke = ''
    for i, ma in enumerate(zma):
        if ma in suffix_code:
            stroke += suffix_code[ma]
            continue

        if i % 2 == 0:
            stroke += lgmb[ma]
        else:
            stroke += rgmb[ma]

    if zma + '简' in codes:
        stroke += suffix_code['正']
    if zma + '正' in codes:
        stroke += suffix_code['简']

    print(f'{zi}\t{stroke}')
