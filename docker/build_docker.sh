#!/bin/bash
# Build the release image for this machine's platform as pinry:local (and
# pinry:<latest git tag>, when there is one). The image isn't published;
# docker-compose.example.yml uses pinry:local.
set -e

script_dir="$( dirname "${0}" )"
version_tag="$(git -C "${script_dir}" tag -l --sort=-creatordate | head -n 1 | sed "s/^v//")"

tags=(-t pinry:local)
if [ -n "${version_tag}" ]; then
    tags+=(-t "pinry:${version_tag}")
fi

docker build "${tags[@]}" \
  -f "${script_dir}/../Dockerfile.autobuild" \
  "${script_dir}/../"
