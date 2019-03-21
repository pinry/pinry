#!/bin/bash

set -e

home_url="http://localhost:$HOST_PORT/"
new_registration_url="http://localhost:$HOST_PORT/register/"
admin_login_url="http://localhost:$HOST_PORT/admin/login/"

echo "Starting container."

$TRAVIS_BUILD_DIR/bootstrap.sh
$TRAVIS_BUILD_DIR/start_docker.sh ${MOUNT_DIR}


sleep 10

# Get status codes
status_code_of_home=`$TRAVIS_BUILD_DIR/tests/http_status_code.sh $home_url`
status_code_of_new_registration=`$TRAVIS_BUILD_DIR/tests/http_status_code.sh $new_registration_url`
status_code_of_admin_login=`$TRAVIS_BUILD_DIR/tests/http_status_code.sh $admin_login_url`

exit_error () {
    echo ${1}
    exit 1
}

assert_equal () {
    [ ${1} = ${2} ] || exit_error "${1} != ${2}, exit now"
}

# enable command echo
set -o xtrace

# Check status codes
case $1 in
  private)
    assert_equal "$status_code_of_home" "302"
    assert_equal "$status_code_of_new_registration" "302"
    assert_equal "$status_code_of_admin_login" "302"
    exit 0
    ;;
  allow_new_registrations)
    assert_equal "$status_code_of_home" "200"
    assert_equal "$status_code_of_new_registration" "200"
    assert_equal "$status_code_of_admin_login" "200"
    exit 0
    ;;
  *)
    echo "$0 $1: invalid option."
    exit 1
esac

exit 1
