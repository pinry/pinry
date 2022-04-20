#!/bin/bash

script_dir="$( dirname "${0}" )"

sudo docker buildx build \
  --push \
  --platform linux/arm/v7,linux/arm64/v8,linux/amd64 \
  -t getpinry/pinry:${@} "${script_dir}/../" \
  -f "${script_dir}/../Dockerfile.autobuild"
