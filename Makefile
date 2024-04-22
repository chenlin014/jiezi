dm-method=0,1,-2,-1
dm-tag=abyz
system=dict-gen/abc.json
chordmap=chordmap/cl.tsv

char-stds=zt jt
programs=rime plover
dictionaries=$(foreach std,$(char-stds),$(foreach program,$(programs),$(program)-$(std)))

common-char-zt=char_set/zt-jia
common-char-jt=char_set/jt-common

char-freq-zt=$$HOME/data/lang/zh/char_freq/zt.csv
char-freq-jt=$$HOME/data/lang/zh/char_freq/jt.csv

jm-name-zt=簡碼
jm-name-jt=简码
jianma-methods=0,-1:-1,0:0,1:1,0:-2,-1:-1,-2

.PHONY: all clean

all: $(dictionaries)

rime-%: build-%
	cat build/$(dm-tag)-$*.tsv | dict-gen/format.sh rime > build/rime-$*.tsv
	printf "\n# $(jm-name-$(*))\n" >> build/rime-$*.tsv
	cat build/jianma-$*.tsv | dict-gen/format.sh rime >> build/rime-$*.tsv
	cat table/punctuation.tsv | dict-gen/format.sh preprocess | \
		python dict-gen/gen_dict.py $(system) $(chordmap) | \
		dict-gen/format.sh algebra > build/rime-punct

plover-%: build-%
	cat build/$(dm-tag)-$*.tsv | dict-gen/format.sh plover > build/plover-$*.json
	cat build/jianma-$*.tsv | dict-gen/format.sh plover > build/plover-jm-$*.json

build-%: daima jianma-%
	cat table/xingzheng-$(dm-tag).tsv | \
		python char_priority/apply_priority.py char_priority/$(dm-tag)-$*.tsv | \
		./dict-gen/format.sh preprocess | \
		python dict-gen/gen_dict.py $(system) $(chordmap) > build/$(dm-tag)-$*.tsv
	cat table/jianma-$*.tsv | ./dict-gen/format.sh preprocess | \
		python dict-gen/gen_dict.py $(system) $(chordmap) > build/jianma-$*.tsv

daima:
	python util/simp_map.py table/xingzheng.tsv $(dm-method) > table/xingzheng-$(dm-tag).tsv
	if [ -f table/xingzheng-$(dm-tag).diff ]; then \
		patch -d table < table/xingzheng-$(dm-tag).diff || \
			(echo "patch failed xingzheng-$(dm-tag)"; exit 1) \
	fi

jianma-%:
	python util/subset.py $(common-char-$(*)) table/xingzheng.tsv | \
		awk -f jianma/code-ge-3.awk | \
		python jianma/jianma-gen.py $(jianma-methods) --char-freq $(char-freq-$(*)) | \
		sed -E 's/$$/简/' > table/jianma-$*.tsv

clean:
	rm build/*
