#!/usr/bin/env bash
_CURRENT_UID=$(id -u):$(id -g)
sudo CURRENT_UID=${_CURRENT_UID} docker-compose up ${@}
