include .env

jiezi-mb=table/jiezi.tsv
shuru-mb=table/shuru.tsv
jianrong-mb=table/jianrong.tsv
jie2ru=table/jie2ru.tsv

dm-method=0,1,-2,-1
dm-tag=abyz
dai-mb=table/shuru-$(dm-tag).tsv

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
mono-bicode=monokey/bicode/zm_bc.tsv
mono-rules=monokey/rules.tsv

.PHONY: all clean

all: $(foreach program,$(programs),$(program)_all)

rime_all: $(foreach std,$(char-stds),rime-$(std)) rime_zigen rime_mono

rime-%: build-%
	cat build/$(dm-tag)-$*.tsv | mb-tool/format.sh rime > build/rime-$*.tsv
	printf "\n# $(jm-name-$(*))\n" >> build/rime-$*.tsv
	cat build/jianma-$*.tsv | mb-tool/format.sh rime >> build/rime-$*.tsv

rime_punc:
	cat table/punctuation.tsv | perl preprocess.pl | \
		$(dict-gen) $(system-zt) $(chordmap) | \
		mb-tool/format.sh algebra | sed -E 's/\|(.+)\|\|\|/\/\1\/|\//' > build/rime-punct

rime_zigen: build_zigen
	cat build/zigen.tsv | mb-tool/format.sh rime > build/rime-zigen.tsv

rime_mono: rime_mono_table $(foreach std,$(char-stds),rime_mono_jm_$(std))

rime_mono_table: daima
	python mb-tool/transform.py $(mono-bicode) $(dai-mb) -r $(mono-rules) | \
	awk '!seen[$$0]++' > monokey/dict.tsv

rime_mono_jm_%: rime_mono_table common-%
	./mb-tool/code_match.sh '^.{3,}$$' table/common-$*.tsv | \
		python mb-tool/transform.py $(mono-bicode) -r $(mono-rules) | \
		$(jianma-gen) $(mono-jm-methods) --char-freq $(char_freq_$(*)) > monokey/jm-$*.tsv

plover_all: $(foreach std,$(char-stds),plover-$(std))

plover-%: build-%
	cat build/$(dm-tag)-$*.tsv | mb-tool/format.sh plover > build/plover-$*.json
	cat build/jianma-$*.tsv | mb-tool/format.sh plover > build/plover-jm-$*.json

build-%: daima jianma-%
	cat $(dai-mb) | \
		python mb-tool/apply_priority.py char_priority/$(dm-tag)-$*.tsv -u ',重,能,能重' | \
		perl preprocess.pl | \
		$(dict-gen) $(system-$(*)) $(chordmap) > build/$(dm-tag)-$*.tsv
	cat table/jianma-$*.tsv | sed -E 's/$$/简/' | perl preprocess.pl | \
		$(dict-gen) $(system-$(*)) $(chordmap) > build/jianma-$*.tsv

build_zigen:
	cat $(chordmap) | sed 's/\t""$$/\t,a/' | \
		awk '{print $$1"\t{"$$2"}"} $$1 !~ /[重能成简空]/ {print $$1"\t{,"$$2"}"}' | \
		$(dict-gen) $(system-jt) $(chordmap) > build/zigen.tsv

daima: shuruma
	cat $(shuru-mb) | \
		python mb-tool/simp_map.py $(dm-method) > $(dai-mb)
ifneq (,$(wildcard ./table/$(dm-tag)-patch.tsv))
		python mb-tool/combine_dict.py $(dai-mb) table/$(dm-tag)-patch.tsv > build/tmp
		mv -f build/tmp $(dai-mb)
endif
ifdef jie2ru
	python mb-tool/column_repl.py -f $(jie2ru) table/jianrong.tsv -c 1 | \
		python mb-tool/simp_map.py $(dm-method) >> $(dai-mb)
else
	cat table/jianrong.tsv | \
		python mb-tool/simp_map.py $(dm-method) >> $(dai-mb)
endif
	awk -i inplace '!seen[$$0]++' $(dai-mb)

shuruma:
ifdef jie2ru
	cat $(jiezi-mb) | \
		python mb-tool/column_repl.py -f $(jie2ru) -c 1 > $(shuru-mb)
endif

jianma-%: common-%
	./mb-tool/code_match.sh '.{3,}' table/common-$*.tsv | \
		$(jianma-gen) 0:0,0,0:$(jianma-methods) --char-freq $(char_freq_$(*)) | \
		sed -E 's/\t(.)..$$/\t空\1/' > table/jianma-$*.tsv

common-%:
	python mb-tool/combine_dict.py table/jiezi.tsv table/standard-$*.tsv | \
		python mb-tool/subset.py char_set/common-$* -st > build/tmp
ifdef jie2ru
	python mb-tool/column_repl.py -f $(jie2ru) build/tmp -c 1 > table/common-$*.tsv
	rm build/tmp
else
	mv -f build/tmp table/common-$*.tsv
endif

po_patch:
	python mb-tool/combine_dict.py char_priority/$(dm-tag)-zt.tsv char_priority/$(dm-tag)-jp-patch.tsv > char_priority/$(dm-tag)-jp.tsv
	python mb-tool/combine_dict.py char_priority/$(dm-tag)-zt.tsv char_priority/$(dm-tag)-vi-patch.tsv > char_priority/$(dm-tag)-vi.tsv

code_freq: $(foreach std,$(char-stds),code-freq-$(std))

code-freq-%: daima jianma-%
	python mb-tool/code_freq.py $(shuru-mb) $(char_freq_$(*)) > stat/code_freq/$*
	python mb-tool/code_freq.py $(dai-mb) $(char_freq_$(*)) > stat/code_freq/$(dm-tag)-$*
	awk -F'\t' 'length($$2) > 2 {next} 1' $(shuru-mb) > build/tmp
	cat table/jianma-$*.tsv >> build/tmp
	python mb-tool/code_freq.py build/tmp $(char_freq_$(*)) > stat/code_freq/jm-$*
	rm build/tmp

clean:
	rm build/*
