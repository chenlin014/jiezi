#!/bin/sh

cd "$(dirname "$0")"

python jianma-gen.py zgbh-$2.tsv $1 | awk -f len-ge-3.awk
