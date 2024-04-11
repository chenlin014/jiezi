#!/bin/sh

basedir=$(dirname "$0")
keymap='abc.json'
chordmap='cl.tsv'

if [ $# -eq 2 ]; then
	python $basedir/gen_dict.py $basedir/../zg_chord/$chordmap $basedir/$keymap $1 -pt $basedir/../char_priority/abyz-$2.tsv
else
	python $basedir/gen_dict.py $basedir/../zg_chord/$chordmap $basedir/$keymap $1
fi
