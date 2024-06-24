#!/bin/sh

case $1 in
	newvc)
		python mb-tool/subset.py table/jianrong.tsv table/common-patch-$2.tsv --difference |
			python mb-tool/subset.py char_set/common-$2
		;;
	nojm)
		python mb-tool/subset.py char_set/common-$2 table/jianma-$2.tsv -d |
			python mb-tool/subset.py /dev/stdin table/xingzheng.tsv |
			mb-tool/code_match.sh '.{3,}'
		;;
	addvc)
		./mb-tool/code_match.sh $2 table/xingzheng.tsv >> table/jianrong.tsv
		;;
esac
