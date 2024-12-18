#!/bin/sh

env \
  PATH="${HOME}/prefixes/python3.13/bin:${HOME}/prefixes/pypy3.10/bin:${HOME}/.local/bin:/usr/bin:/bin" \
  $@
