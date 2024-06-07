#!/bin/sh

awk -F'\t' -v pattern=$2 '$2 ~ pattern {print $1"\t"$2}' $1
