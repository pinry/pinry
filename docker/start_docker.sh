#!/bin/bash

DATA_PATH=${1}
HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
SETTINGS_PATH="${HERE}/pinry/local_settings.py"

if [ "${DATA_PATH}" = "" ]
then
    echo "usage: start_docker.sh /abs/path/to/your/data/store"
    exit 1
fi

sudo docker run -d=true -p=80:80 \
    -v=${DATA_PATH}:/data \
    pinry/pinry
