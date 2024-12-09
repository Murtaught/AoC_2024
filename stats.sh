#!/bin/sh

set -e

echo "Line count:"
find . -iname "main.*" | sort | xargs wc -l
