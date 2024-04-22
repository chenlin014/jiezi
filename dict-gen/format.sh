#!/bin/sh

case $1 in
	preprocess)
		cat | awk -F'\t' '
		{ 
			if ($2 ~ /\{.+\}/) {
				printf("%s\t%s\n", $1, $2);
			}
			else {
				gsub(/(.)/, "& ", $2);
				gsub(/[ ]+$/, "", $2);
				printf("%s\t%s\n", $1, $2);
			}
		}' | sed -E 's/([^重能简"] [^重能简"])/<\1>/g;
			s/([^>]) 重/\1重/g;
			s/<(.) (.)> 重/<\1重 \2>/g;
			s/(.)> ([能简])/\1\2>/g;
			s/\t<([^空] [^空])>$/\t<成\1>/;' |
		awk -F'\t' '{
			gsub(/[<>]/, "", $2);
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
