#!/bin/bash

gen_key() {
  # Check for secret key if one doesn't exist create.
  if [ ! -f /data/production_secret_key.txt ]
  then
      cd /data
      PRODUCTION_SECRET_KEY=`pwgen -c -n -1 65`
      echo $PRODUCTION_SECRET_KEY > /data/production_secret_key.txt
  else
      PRODUCTION_SECRET_KEY=`cat /data/production_secret_key.txt`
  fi

  echo ${PRODUCTION_SECRET_KEY}
}
gen_key
