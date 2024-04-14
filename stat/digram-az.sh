#!/bin/sh

cat $1 | awk '{
	n=split($3,freqs,",");
	total = freqs[1] + freqs[n];
	printf("%s\t%d\t%d,%d\n", $1, total, freqs[1], freqs[n]);
}' | sort -k 2 -n -r
