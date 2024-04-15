#!/bin/sh

case $1 in
	sscode)
		cat | awk '{
			gsub(/./, "& ", $2);
			gsub(/[ ]+$/, "", $2);
			printf("%s\t%s\n", $1, $2);
		}'
		;;
	rime)
		cat | sed 's/<>//g; s/ | //g'
		;;
	algebra)
		cat | sed 's/<>//g; s/ | //g' | sed -E 's/(.+)\t(.+)/- xform|^\2$|\1|/'
		;;
	plover)
		echo "{"
		cat | sed 's/ | /\//g; s/<>//g' |
			sed -E 's/(.+)\t(.+)/"\2": "\1",/' |
			sed -E '$ s/,$//' |
			perl -pe 's/: "(?!(\{.+\}|=))/: "{&/g;' |
			sed -E 's/: "\{&(.+)"/: "\{\&\1}"/'
		echo "}"
		;;
esac
