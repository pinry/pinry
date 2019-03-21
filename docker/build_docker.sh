#!/bin/bash

script_dir="$( dirname "${0}" )"
sudo docker build -t pinry/pinry${@} "${script_dir}/../" -f "${script_dir}/../Dockerfile.autobuild"
