# 用字标准
# zt: 正體（繁體）
# jt: 简体
# jp: 日文
char-standards=zt jt jp

# == 码表路径 ==
# 初解表
init-mb = table/chujie.tsv

mb-xformer=python mb-tool/mb_algebra.py --regex

.PHONY: all clean

all: xingyi siyuan

build:
	mkdir $@

xingyi: $(foreach std,$(char-standards),xingyi-$(std))

xingyi-%:
	cat $(init-mb) | $(mb-xformer) mb-algebra/xingyi-$*.yaml | \
		$(mb-xformer) mb-algebra/xingyi.yaml | \
		$(mb-xformer) mb-algebra/common.yaml > table/xingyi-$*.tsv

siyuan: build
	cat $(init-mb) | $(mb-xformer) mb-algebra/siyuan.yaml | \
		$(mb-xformer) mb-algebra/common.yaml > table/siyuan.tsv

shuruma:
	cat $(init-mb) | $(mb-xformer) $(xform-dir)/varied.yaml | \
		$(mb-xformer) $(xform-dir)/unvaried.yaml > $(shuru-mb)

common-%:
	python mb-tool/subset.py $(init-mb) char_set/common-$* | \
		$(mb-xformer) $(xform-dir)/standard-$*.yaml | \
		$(mb-xformer) $(xform-dir)/unvaried.yaml > table/common-$*.tsv
