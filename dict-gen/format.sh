#!/bin/sh

case $1 in
	rime)
		cat | sed 's/,//g' | sed 's/ //g'
		;;
	algebra)
		cat | sed -E 's/[ ,]//g' | sed -E 's/(.+)\t(.+)/- xform|^\2$|\1|/'
		;;
	plover)
		echo "{"
		cat | sed 's/ /\//g; s/,//g' | sed -E 's/(.+)\t(.+)/"\2": "{\&\1}",/' | sed '$ s/",/"/'
		echo "}"
		;;
esac
