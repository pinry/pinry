#!/bin/bash

script_dir="$( dirname "${0}" )"
sudo docker build -t getpinry/pinry${@} "${script_dir}/../" \
  -f "${script_dir}/../Dockerfile.autobuild"
