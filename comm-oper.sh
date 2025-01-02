#!/bin/sh

case $1 in
	nojm)
		python mb-tool/subset.py char_set/common-$2 steno/steno-jm-$2.tsv -d |
			python mb-tool/subset.py -st /dev/stdin table/jiezi.tsv |
			mb-tool/code_match.sh '.{3,}'
		;;
	checkpo)
		python mb-tool/check_priority.py steno/char_priority/abyz-$2.tsv table/shuru-abyz.tsv
		;;
esac
