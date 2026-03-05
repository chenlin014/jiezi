# 用字标准
# zt: 正體（繁體）
# jt: 简体
# jp: 日文
char-standards=ft jt jp

# == 码表路径 ==
# 初解表
init-mb = table/chujie.tsv

mb-xformer=python mb-tool/mb_algebra.py --regex

.PHONY: all clean

all: xingyi siyuan huaiyuan

xingyi: $(foreach std,$(char-standards),xingyi-$(std))

xingyi-%:
	cat $(init-mb) | \
		$(mb-xformer) mb-algebra/common-pre.yaml | \
		$(mb-xformer) mb-algebra/xingyi-$*.yaml | \
		$(mb-xformer) mb-algebra/xingyi.yaml | \
		$(mb-xformer) mb-algebra/common-serial.yaml | \
		$(mb-xformer) mb-algebra/common-post.yaml > table/xingyi-$*.tsv

siyuan:
	cat $(init-mb) | \
		$(mb-xformer) mb-algebra/common-pre.yaml | \
		$(mb-xformer) mb-algebra/siyuan.yaml | \
		$(mb-xformer) mb-algebra/common-serial.yaml | \
		$(mb-xformer) mb-algebra/common-post.yaml > table/siyuan.tsv

huaiyuan:
	cat $(init-mb) | \
		$(mb-xformer) mb-algebra/common-pre.yaml | \
		$(mb-xformer) mb-algebra/huaiyuan.yaml | \
		$(mb-xformer) mb-algebra/common-post.yaml | \
		$(mb-xformer) mb-algebra/huaiyuan.yaml > table/huaiyuan.tsv
