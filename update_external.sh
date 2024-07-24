#!/bin/sh

set -a
source ./.env
set +a

rime_header () {
	awk '/^\.\.\.$/ { exit }1' $1
	echo '...'
	echo ''
}

make

rime_header $rime_dir/xingzheng-zt.dict.yaml > build/temp
cat build/rime-zt.tsv >> build/temp
cp -f build/temp $rime_dir/xingzheng-zt.dict.yaml

rime_header $rime_dir/xingzheng-jt.dict.yaml > build/temp
cat build/rime-jt.tsv >> build/temp
cp -f build/temp $rime_dir/xingzheng-jt.dict.yaml

rime_header $rime_dir/mono-xingzheng.dict.yaml > build/temp
python mb-tool/apply_mapping.py monokey/codemap/yuan.json monokey/keymap/qwerty.json monokey/dict.tsv |
	awk -f monokey/add_stem.awk >> build/temp
cp -f build/temp $rime_dir/mono-xingzheng.dict.yaml

rime_header $rime_dir/mono-xingzheng-jm-zt.dict.yaml > build/temp
python mb-tool/apply_mapping.py monokey/codemap/yuan.json monokey/keymap/qwerty.json monokey/jm-zt.tsv >> build/temp
cp -f build/temp $rime_dir/mono-xingzheng-jm-zt.dict.yaml

rime_header $rime_dir/mono-xingzheng-jm-jt.dict.yaml > build/temp
python mb-tool/apply_mapping.py monokey/codemap/yuan.json monokey/keymap/qwerty.json monokey/jm-jt.tsv >> build/temp
cp -f build/temp $rime_dir/mono-xingzheng-jm-jt.dict.yaml

rm build/temp
