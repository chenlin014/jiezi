#!/bin/sh

case $1 in
	checkstd)
		python mb-tool/subset.py table/jianrong.tsv table/standard-$2.tsv --difference
		echo ""
		python mb-tool/find_duplicate.py table/standard-$2.tsv -r
		;;
	nojm)
		python mb-tool/subset.py char_set/common-$2 table/jianma-$2.tsv -d |
			python mb-tool/subset.py /dev/stdin table/xingzheng.tsv |
			mb-tool/code_match.sh '.{3,}'
		;;
	addvc)
		./mb-tool/code_match.sh $2 table/xingzheng.tsv >> table/jianrong.tsv
		;;
	checkpo)
		python mb-tool/check_priority.py char_priority/abyz-$2.tsv table/xingzheng-abyz.tsv
		;;
esac
