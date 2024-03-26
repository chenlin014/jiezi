#!/bin/sh

cat | sed -E 's/(.+)\t(.+)/- "xform|^\2$|\1|"/'
