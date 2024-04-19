dm-method=0,1,-2,-1
dm-tag=abyz
system=dict-gen/abc.json
chordmap=chordmap/cl.tsv

char-stds=zt jt
programs=rime plover
dictionaries=$(foreach std,$(char-stds),$(foreach program,$(programs),$(program)-$(std)))

char-freq-zt=$$HOME/data/lang/zh/char_freq/zt.csv
char-freq-jt=$$HOME/data/lang/zh/char_freq/jt.csv

common-char-zt=char_set/zt-jia
common-char-jt=char_set/jt-common

jm-name-zt=簡碼
jm-name-jt=简码

.PHONY: all clean

all: $(dictionaries)

rime-%: build-%
	cat build/$(dm-tag)-$*.tsv | dict-gen/format.sh rime > build/rime-$*.tsv
	printf "\n# $(jm-name-$(*))\n" >> build/rime-$*.tsv
	cat build/jianma-$*.tsv | dict-gen/format.sh rime >> build/rime-$*.tsv

plover-%: build-%
	cat build/$(dm-tag)-$*.tsv | dict-gen/format.sh plover > build/plover-$*.json
	cat build/jianma-$*.tsv | dict-gen/format.sh plover > build/plover-jm-$*.json

build-%: daima jianma-%
	cat table/xingzheng-$(dm-tag).tsv | ./dict-gen/format.sh sscode | \
		python dict-gen/gen_dict.py $(system) $(chordmap) -pt char_priority/$(dm-tag)-$*.tsv > \
		build/$(dm-tag)-$*.tsv
	cat table/jianma-$*.tsv | ./dict-gen/format.sh code2split | \
		python dict-gen/gen_dict.py $(system) $(chordmap) -pt char_priority/jm-$*.tsv > \
		build/jianma-$*.tsv

daima:
	python util/simp_map.py table/xingzheng.tsv $(dm-method) > table/xingzheng-$(dm-tag).tsv
	if [ -f table/xingzheng-$(dm-tag).diff ]; then \
		patch -d table < table/xingzheng-$(dm-tag).diff || \
			(echo "patch failed xingzheng-$(dm-tag)"; exit 1) \
	fi

jianma-%:
	python util/subset.py table/xingzheng.tsv $(common-char-$(*)) | \
		python jianma/jianma-gen.py jianma/zgbh-$*.tsv | \
		awk -f jianma/code-ge-3.awk > table/jianma-$*.tsv
	python util/check_map.py table/jianma-$*.tsv | tail -n +2 | \
		python jianma/priority-gen.py $(char-freq-$(*)) > char_priority/jm-$*.tsv

clean:
	rm build/*
