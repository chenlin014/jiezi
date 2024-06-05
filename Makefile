dm-method=0,1,-2,-1
dm-tag=abyz

dict-gen=python mb-tool/steno_dict.py
system=system/abc.json
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

az=0,-1
ab=0,1
yz=-2,-1
za=-1,0
ba=1,0
zy=-1,-2
jianma-methods=$(az):$(ab):$(yz):$(za):$(ba):$(zy)

.PHONY: all clean

all: $(foreach program,$(programs),$(program)_all) shintei

rime_all: $(foreach std,$(char-stds),rime-$(std)) rime_punc rime_zigen

rime-%: build-%
	cat build/$(dm-tag)-$*.tsv | mb-tool/format.sh rime > build/rime-$*.tsv
	printf "\n# $(jm-name-$(*))\n" >> build/rime-$*.tsv
	cat build/jianma-$*.tsv | mb-tool/format.sh rime >> build/rime-$*.tsv

rime_punc:
	cat table/punctuation.tsv | mb-tool/format.sh preprocess | \
		$(dict-gen) $(system) $(chordmap) | \
		mb-tool/format.sh algebra > build/rime-punct

rime_zigen: build_zigen
	cat build/zigen.tsv | mb-tool/format.sh rime > build/rime-zigen.tsv

plover_all: $(foreach std,$(char-stds),plover-$(std))

plover-%: build-%
	cat build/$(dm-tag)-$*.tsv | mb-tool/format.sh plover > build/plover-$*.json
	cat build/jianma-$*.tsv | mb-tool/format.sh plover > build/plover-jm-$*.json

build-%: daima jianma-%
	cat table/xingzheng-$(dm-tag).tsv | \
		python mb-tool/apply_priority.py char_priority/$(dm-tag)-$*.tsv -u ',重,能,重能' | \
		./mb-tool/format.sh preprocess | \
		$(dict-gen) $(system) $(chordmap) > build/$(dm-tag)-$*.tsv
	cat table/jianma-$*.tsv | sed -E 's/$$/简/' | ./mb-tool/format.sh preprocess | \
		$(dict-gen) $(system) $(chordmap) > build/jianma-$*.tsv

build_zigen:
	cat $(chordmap) | sed 's/\t""$$/\t,a/' | \
		awk '{print $$1"\t{"$$2"}"} $$1 !~ /[重能成简空]/ {print $$1"\t{,"$$2"}"}' | \
		$(dict-gen) $(system) $(chordmap) > build/zigen.tsv

daima:
	python mb-tool/simp_map.py table/xingzheng.tsv $(dm-method) > table/xingzheng-$(dm-tag).tsv
	if [ -f table/xingzheng-$(dm-tag).diff ]; then \
		patch -d table < table/xingzheng-$(dm-tag).diff || \
			(echo "patch failed xingzheng-$(dm-tag)"; exit 1) \
	fi

jianma-%:
	python mb-tool/subset.py $(common-char-$(*)) table/xingzheng-$(dm-tag).tsv | \
		awk -f jianma/code-ge-3.awk | \
		python jianma/jianma-gen.py 0:0,0,0:$(jianma-methods) --char-freq $(char-freq-$(*)) | \
		sed -E 's/\t(.)..$$/\t空\1/' > table/jianma-$*.tsv

shintei:
	cat table/xingzheng-$(dm-tag).tsv | \
		python mb-tool/apply_priority.py char_priority/$(dm-tag)-jp.tsv -u ',重,能,重能' | \
		./mb-tool/format.sh preprocess | \
		$(dict-gen) system/yayakana.json $(chordmap) | \
		./mb-tool/format.sh rime | \
		sed -E 's/\t(.+)y$$/\ta\1/; s/\t/\tj/' > build/rime-shintei.tsv

clean:
	rm build/*
