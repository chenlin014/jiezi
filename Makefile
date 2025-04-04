# 用字标准
# zt: 正體（繁體）
# jt: 简体
# jp: 日文
char-standards=zt jt jp

# == 码表路径 ==
# 初解表
init-mb = table/chujie.tsv
# 输入码表。生成自初始码表。
shuru-mb=table/shuru.tsv

mb-xformer=python mb-tool/mb_algebra.py --regex
xform-dir=mb-algebra

.PHONY: all clean

all: shuruma $(foreach std,$(char-standards),common-$(std))

shuruma:
	cat $(init-mb) | $(mb-xformer) $(xform-dir)/varied.yaml | \
		$(mb-xformer) $(xform-dir)/unvaried.yaml > $(shuru-mb)

common-%:
	python mb-tool/subset.py table/jiezi.tsv char_set/common-$* | \
		$(mb-xformer) $(xform-dir)/standard-$*.yaml | \
		$(mb-xformer) $(xform-dir)/unvaried.yaml > table/common-$*.tsv

clean:
	rm build/*
