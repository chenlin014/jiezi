#!/bin/sh

keymap='dict-gen/abc.json'
chordmap='zg_chord/cl.tsv'

cd $(dirname "$0")

if [ $# -eq 2 ]; then
	cat $1 | ./dict-gen/format.sh sscode | python dict-gen/gen_dict.py $chordmap $keymap -pt char_priority/abyz-$2.tsv
else
	cat $1 | ./dict-gen/format.sh sscode | python dict-gen/gen_dict.py $chordmap $keymap
fi
