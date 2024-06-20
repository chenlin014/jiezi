#!/bin/sh

case $1 in
	newvc)
		python mb-tool/subset.py table/jianrong.tsv table/common-patch-$2.tsv --difference |
			python mb-tool/subset.py char_set/common-$2
esac
