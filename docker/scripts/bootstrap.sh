#!/bin/bash

gen_key() {
  echo "=================================================================================="
  echo "Note: Please copy this key and keep it in a secure place."
  echo "Then you should manually edit your pinry/local_settings.py"
  echo "and replace SECRET_KEY with new secret-key if you had previously generated a"
  echo "pinry/local_settings.py."
  echo "If no previous pinry/local_settings.py generated, you can have a look and edit it."
  echo "If you want to use docker-compose, just edit docker-compose.yml and use 'docker-compose up'"

  SECRET_KEY=$(bash /pinry/docker/scripts/gen_key.sh)

  echo ""
  echo "Your secret-key is(also saved/overwritten your docker's /data/production_secret_key.txt):"
  echo ""
  echo ${SECRET_KEY}
  echo "=================================================================================="
}

local_settings_file="/data/local_settings.py"
# Create local_settings.py
if [ ! -f "${local_settings_file}" ];
then
    cp "/pinry/pinry/settings/local_settings.example.py" "${local_settings_file}"
    gen_key
    sed -i "s/secret\_key\_place\_holder/${SECRET_KEY}/" "${local_settings_file}"
fi

cp "${local_settings_file}" "/pinry/pinry/settings/local_settings.py"
