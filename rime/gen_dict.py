import sys, json, csv, re

if len(sys.argv) != 4:
    print('Usage: gen_dict <char_mb> <zigen_mb> <keymap>')
    quit()
_, mb_path, gmb_path, km_path = sys.argv

with open(mb_path) as f:
    reader = csv.reader(f, delimiter='\t')
    mb = [(zi, ma) for zi, ma in reader]

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
lgmb['重'] = km[2][2]
rgmb['重'] = km[2][2]
lgmb['能'] = km[2][3]
rgmb['能'] = km[2][3]

for zi, ma in mb:
    code = ''
    for i, m in enumerate(ma):
        if i % 2 == 0:
            code += lgmb[m]
        else:
            code += rgmb[m]

    print(f'{zi}\t{code}')
