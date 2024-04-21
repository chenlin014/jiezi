#!/bin/sh

case $1 in
	sscode)
		if [ -z "$2" ]; then
			gs=1
		else
			gs=$2
		fi

		cat | awk -F'\t' -v group_size=$gs '
		BEGIN { regex = "(.{"group_size"})" }
		{ 
			if ($2 ~ /\{.+\}/) {
				printf("%s\t%s\n", $1, $2);
			}
			else {
				gsub(regex, "& ", $2);
				gsub(/[ ]+$/, "", $2);
				printf("%s\t%s\n", $1, $2);
			}
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
