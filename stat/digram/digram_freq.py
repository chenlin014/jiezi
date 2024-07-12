import sys, csv

def main():
    try:
        _, mb_file = sys.argv
    except:
        print(f'Usage: {sys.argv[0]} <码表>')
        quit()

    with open(mb_file, encoding='utf_8') as f:
        reader = csv.reader(f, delimiter='\t')
        codes = [code for _, code in reader]

    max_code_len = max(len(code) for code in codes)
    digram_freqs = dict()

    for code in codes:
        for i in range(len(code)-1):
            dg = code[i:i+2]
            if dg in digram_freqs:
                ind = i if i + 1 <= len(code) / 2 else i - len(code) + 1
                digram_freqs[dg][ind] += 1
            else:
                digram_freqs[dg] = [0] * (max_code_len-1)
                digram_freqs[dg][i] = 1

    ranking = [(digram, sum(freqs)) for digram, freqs in digram_freqs.items()]
    ranking.sort(reverse=True, key=lambda x: x[1])

    for digram, freq in ranking:
        print(f'{digram}\t{freq}\t{",".join(str(f) for f in digram_freqs[digram])}')

if __name__ == '__main__':
    main()
