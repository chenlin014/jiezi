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
    mb = [(zi, ma) for zi, ma in reader]

lgmb['重'] = km[2][2]
rgmb['重'] = km[2][2]
lgmb['能'] = km[2][3]
rgmb['能'] = km[2][3]
for zi, zma in mb:
    stroke = ''
    for i, ma in enumerate(zma):
        if i % 2 == 0:
            stroke += lgmb[ma]
        else:
            stroke += rgmb[ma]

    print(f'{zi}\t{stroke}')
