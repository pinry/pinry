#!/bin/bash

script_dir="$( dirname "${0}" )"

IMAGE_LATEST_TAG="latest"
IMAGE_VERSION_TAG=`git tag -l --sort=-creatordate | head -n 1 | sed "s/v//g"`

sudo docker buildx build \
  --push \
  --platform linux/arm/v7,linux/arm64/v8,linux/amd64 \
  -t getpinry/pinry:${IMAGE_LATEST_TAG} "${script_dir}/../" \
  -f "${script_dir}/../Dockerfile.autobuild"

sudo docker buildx build \
  --push \
  --platform linux/arm/v7,linux/arm64/v8,linux/amd64 \
  -t getpinry/pinry:${IMAGE_VERSION_TAG} "${script_dir}/../" \
  -f "${script_dir}/../Dockerfile.autobuild"
