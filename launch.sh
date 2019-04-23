#!/bin/bash -e
docker build -q -t battlechess -f Dockerfile .   # 1>&2
docker run -i --rm battlechess bash -c "cd /tmp/ && git clone -q https://github.com/$1/battlechess.git && python3 /tmp/battlechess/engine.py"

