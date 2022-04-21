#!/bin/bash

script_dir="$( dirname "${0}" )"

IMAGE_TAG="latest"

# shellcheck disable=SC2199
if [[ "${@}" != "" ]];then
    # shellcheck disable=SC2124
    IMAGE_TAG="${@}"
fi

sudo docker buildx build \
  --push \
  --platform linux/arm/v7,linux/arm64/v8,linux/amd64 \
  -t getpinry/pinry:${IMAGE_TAG} "${script_dir}/../" \
  -f "${script_dir}/../Dockerfile.autobuild"
