#!/bin/bash

script_dir="$( dirname "${0}" )"
# Force users to login before seeing any pins.
if [ "${ALLOW_NEW_REGISTRATIONS}" = "" ]; then
    ALLOW_NEW_REGISTRATIONS=true
fi

if [[ "$(docker images -q pinry/pinry 2> /dev/null)" == "" ]]; then
  echo "No docker image found, building..." && "${script_dir}/build_docker.sh"
fi

echo "=================================================================================="
echo "Note: Please copy this key and keep it in a secure place."
echo "Then you should manually edit your pinry/local_settings.py"
echo "and replace SECRET_KEY with new secret-key if you had previously generated a"
echo "pinry/local_settings.py."
echo "If no previous pinry/local_settings.py generated, you can have a look and edit it."
echo "If you want to use docker-compose, just edit docker-compose.yml and use 'docker-compose up'"

SECRET_KEY=$(sudo docker run pinry/pinry /scripts/gen_key.sh)

echo ""
echo "Your secret-key is(also saved/overwritten your pinry/production_secret_key.txt):"
echo ""
echo ${SECRET_KEY}
echo "=================================================================================="

local_settings_file="${script_dir}/pinry/local_settings.py"
# Create local_settings.py
if [ ! -f "${local_settings_file}" ];
then
    cp "${script_dir}/pinry/local_settings.example.py" "${local_settings_file}"
    sed -i "s/secret\_key\_place\_holder/${SECRET_KEY}/" "${local_settings_file}"

    # Force users to login before seeing any pins.
    if [ "${PRIVATE}" = "true" ]; then
        sed -i "s/PUBLIC = True/PUBLIC = False/" "${local_settings_file}"
    fi

    # Enable people from creating new accounts.
    if [ "${ALLOW_NEW_REGISTRATIONS}" = "true" ]; then
        sed -i "s/ALLOW_NEW_REGISTRATIONS = False/ALLOW_NEW_REGISTRATIONS = True/" "${local_settings_file}"
    fi
fi

# Copy to docker-compose.yml
if [ ! -f "${script_dir}/docker-compose.yml" ];
then
    cp "${script_dir}/docker-compose.example.yml" "${script_dir}/docker-compose.yml"
fi
