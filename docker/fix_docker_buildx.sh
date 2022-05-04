#!/bin/bash
# from here: https://stackoverflow.com/questions/60080264/docker-cannot-build-multi-platform-images-with-docker-buildx
sudo docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
sudo docker buildx rm builder
sudo docker buildx create --name builder --driver docker-container --use
sudo docker buildx inspect --bootstrap
