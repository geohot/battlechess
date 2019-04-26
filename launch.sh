#!/bin/bash -e
docker build -t battlechess -f Dockerfile .   # 1>&2
if [ ! -z $1 ]; then
  docker run -i --rm battlechess bash -c "cd /tmp/ && git clone -q https://github.com/$1/battlechess.git && cd battlechess && python3 engine.py"
fi

