#!/bin/bash -e
docker build -t battlechess -f Dockerfile .   # 1>&2

# TODO: sandbox the python3 process more aggressively
docker run -i --security-opt seccomp=seccomp.json --rm battlechess bash -c "cd /tmp/ && git clone -q https://github.com/$1/battlechess.git && python3 /tmp/battlechess/engine.py"

