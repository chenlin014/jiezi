include .env

dm-method=0,1,-2,-1
dm-tag=abyz

dict-gen=python mb-tool/steno_dict.py
chordmap=chordmap/cl.tsv

system-zt=system/abc.json
system-jt=system/abc.json
system-jp=system/yayakana.json

jianma-gen=python mb-tool/jianma-gen.py

char-stds=zt jt jp
programs=rime plover
dictionaries=$(foreach std,$(char-stds),$(foreach program,$(programs),$(program)-$(std)))

jm-name-zt=簡碼
jm-name-jt=简码
jm-name-jp=略コード

az=0,-1
ab=0,1
yz=-2,-1
za=-1,0
ba=1,0
zy=-1,-2
jianma-methods=$(az):$(ab):$(za):$(ba):$(yz):$(zy)

mono-jm-methods=0:0,1,2:0,1,-1
mono-zg-code=monokey/zg_code.tsv
mono-rules=monokey/rules.tsv

.PHONY: all clean

all: $(foreach program,$(programs),$(program)_all)

rime_all: $(foreach std,$(char-stds),rime-$(std)) rime_zigen rime_mono

rime-%: build-%
	cat build/$(dm-tag)-$*.tsv | mb-tool/format.sh rime > build/rime-$*.tsv
	printf "\n# $(jm-name-$(*))\n" >> build/rime-$*.tsv
	cat build/jianma-$*.tsv | mb-tool/format.sh rime >> build/rime-$*.tsv

rime_punc:
	cat table/punctuation.tsv | mb-tool/format.sh preprocess | \
		$(dict-gen) $(system-zt) $(chordmap) | \
		mb-tool/format.sh algebra | sed -E 's/\|(.+)\|\|\|/\/\1\/|\//' > build/rime-punct

rime_zigen: build_zigen
	cat build/zigen.tsv | mb-tool/format.sh rime > build/rime-zigen.tsv

rime_mono: rime_mono_table $(foreach std,$(char-stds),rime_mono_jm_$(std)) rime_mono_jm_jp

rime_mono_table: daima
	python mb-tool/transform.py $(mono-zg-code) table/xingzheng-$(dm-tag).tsv -r $(mono-rules) | \
	awk '!seen[$$0]++' > monokey/dict.tsv

rime_mono_jm_%: rime_mono_table common-%
	./mb-tool/code_match.sh '^.{3,}$$' table/common-$*.tsv | \
		python mb-tool/transform.py $(mono-zg-code) -r $(mono-rules) | \
		$(jianma-gen) $(mono-jm-methods) --char-freq $(char_freq_$(*)) > monokey/jm-$*.tsv

plover_all: $(foreach std,$(char-stds),plover-$(std))

plover-%: build-%
	cat build/$(dm-tag)-$*.tsv | mb-tool/format.sh plover > build/plover-$*.json
	cat build/jianma-$*.tsv | mb-tool/format.sh plover > build/plover-jm-$*.json

build-%: daima jianma-%
	cat table/xingzheng-$(dm-tag).tsv | \
		python mb-tool/apply_priority.py char_priority/$(dm-tag)-$*.tsv -u ',重,能,重能' | \
		awk -f preprocess.awk | \
		$(dict-gen) $(system-$(*)) $(chordmap) > build/$(dm-tag)-$*.tsv
	cat table/jianma-$*.tsv | sed -E 's/$$/简/' | awk -f preprocess.awk | \
		$(dict-gen) $(system-$(*)) $(chordmap) > build/jianma-$*.tsv

build_zigen:
	cat $(chordmap) | sed 's/\t""$$/\t,a/' | \
		awk '{print $$1"\t{"$$2"}"} $$1 !~ /[重能成简空]/ {print $$1"\t{,"$$2"}"}' | \
		$(dict-gen) $(system-jt) $(chordmap) > build/zigen.tsv

daima:
	cat table/xingzheng.tsv table/jianrong.tsv | \
		python mb-tool/simp_map.py $(dm-method) | \
		awk '!seen[$$0]++' > table/xingzheng-$(dm-tag).tsv
	if [ -f table/xingzheng-$(dm-tag).diff ]; then \
		patch -d table < table/xingzheng-$(dm-tag).diff || \
			(echo "patch failed xingzheng-$(dm-tag)"; exit 1) \
	fi

jianma-%: common-%
	./mb-tool/code_match.sh '.{3,}' table/common-$*.tsv | \
		$(jianma-gen) 0:0,0,0:$(jianma-methods) --char-freq $(char_freq_$(*)) | \
		sed -E 's/\t(.)..$$/\t空\1/' > table/jianma-$*.tsv

common-%:
	python mb-tool/subset.py table/standard-$*.tsv char_set/common-$* > build/tmp
	python mb-tool/subset.py table/xingzheng-$(dm-tag).tsv char_set/common-$* | \
		python mb-tool/combine_dict.py build/tmp --stdin > table/common-$*.tsv
	rm build/tmp

po_patch:
	python mb-tool/combine_dict.py char_priority/$(dm-tag)-zt.tsv char_priority/$(dm-tag)-jp-patch.tsv > char_priority/$(dm-tag)-jp.tsv
	python mb-tool/combine_dict.py char_priority/$(dm-tag)-zt.tsv char_priority/$(dm-tag)-vi-patch.tsv > char_priority/$(dm-tag)-vi.tsv

code_freq: $(foreach std,$(char-stds),code-freq-$(std))

code-freq-%: daima jianma-%
	python mb-tool/code_freq.py table/xingzheng.tsv $(char_freq_$(*)) > stat/code_freq/$*
	python mb-tool/code_freq.py table/xingzheng-$(dm-tag).tsv $(char_freq_$(*)) > stat/code_freq/$(dm-tag)-$*
	awk -F'\t' 'length($$2) > 2 {next} 1' table/xingzheng.tsv > build/tmp
	cat table/jianma-$*.tsv >> build/tmp
	python mb-tool/code_freq.py build/tmp $(char_freq_$(*)) > stat/code_freq/jm-$*
	rm build/tmp

clean:
	rm build/*
