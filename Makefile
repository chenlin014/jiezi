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

a=0:0,0
ab=0,1:1,0
ac=0,2:2,0
ax=0,-3:-3,0
ay=0,-2:-2,0
az=0,-1:-1,0
b=1:1,1
bc=1,2:2,1
bx=1,-3:-3,1
by=1,-2:-2,1
bz=1,-1:-1,1
c=2:2,2
cx=2,-3:-3,2
cy=2,-2:-2,2
cz=2,-1:-1,2
x=-3:-3,-3
xy=-3,-2:-2,-3
xz=-3,-1:-1,-3
y=-2:-2,-2
yz=-2,-1:-1,-2
z=-1:-1,-1
jianma-methods=$(az):$(ab):$(yz)

.PHONY: all clean

all: $(dictionaries)

rime-%: build-% rime_punc
	cat build/$(dm-tag)-$*.tsv | dict-gen/format.sh rime > build/rime-$*.tsv
	printf "\n# $(jm-name-$(*))\n" >> build/rime-$*.tsv
	cat build/jianma-$*.tsv | dict-gen/format.sh rime >> build/rime-$*.tsv

rime_punc:
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
	cat table/jianma-$*.tsv | sed -E 's/$$/简/' | ./dict-gen/format.sh preprocess | \
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
		python jianma/jianma-gen.py $(jianma-methods) --char-freq $(char-freq-$(*)) > \
		table/jianma-$*.tsv

clean:
	rm build/*
