#!/usr/bin/env bash
CURRENT_UID=$(id -u):$(id -g) sudo docker-compose up ${@}
