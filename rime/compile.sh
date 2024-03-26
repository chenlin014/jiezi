#!/bin/sh

basedir=$(dirname "$0")
keymap='abc.json'
chordmap='cl.tsv'

case $2 in
	algebra)
		python $basedir/gen_dict.py $basedir/../zg_chord/$chordmap $basedir/$keymap $1 | sed -E 's/(.+)\t(.+)/- xform|^\2$|\1|/'
		;;
	*)
		python $basedir/gen_dict.py $basedir/../zg_chord/$chordmap $basedir/$keymap $1
		;;
esac
