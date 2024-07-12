import sys, readline

table_paths = sys.argv[1:]

tables = dict()

for path in table_paths:
    with open(path) as f:
        tables[path] = [line.split('\t') for line in
            f.read().splitlines() if line]

while True:
    search = input('> ').strip()

    if not search:
        break

    for path in table_paths:
        for i, row in enumerate(tables[path]):
            if row[0] == search:
                print(path)
                print(f'\t{i+1}: {"\t".join(row)}')
                break

    print()
