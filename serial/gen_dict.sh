#!/bin/sh

python mb-tool/apply_mapping.py monokey/codemap/$1.json monokey/keymap/$2.json $3 | awk -f monokey/add_stem.awk
