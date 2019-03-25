#!/bin/bash

set -e

usage() {
  cat <<EOL
USAGE: $(basename $0) url
OPTIONS:
  -h, --help
EOL
    exit 1
}

main() {
    local argc=0
    local argv=()

    while [ $# -gt 0 ]; do
        case $1 in
            -h|--help)
                usage
                ;;
            *)
                argc=`expr $argc + 1`
                argv+=($1)
                ;;
        esac
  
        shift
    done

    if [ $argc -lt 1 ]; then
        echo "Too few arguments"
        exit 1
    fi

    url=${argv[0]}
    http_status_code=`curl -s -w "%{http_code}" -o /dev/null $url`
    echo $http_status_code
}

main $*
