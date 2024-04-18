#!/bin/sh

cd "$(dirname "$0")"

cat | python ../util/check_map.py |
	tail -n +2 | python priority-gen.py $1
