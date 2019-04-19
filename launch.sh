#!/bin/bash -e
echo "hello $0 $1" > /dev/stderr
docker build -t battlechess -f Dockerfile .   # 1>/dev/stderr
docker run -i --rm battlechess bash -c "cd /tmp/ && git clone https://github.com/$1/battlechess.git && python3 /tmp/battlechess/engine.py"

