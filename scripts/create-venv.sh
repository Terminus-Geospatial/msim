#!/usr/bin/env bash

set -e

#  Python Version
PYTHON_EXE="python"

#  Path to venv
VENV_PATH='./venv'

#------------------------------------------------#
#-      Check the current python version        -#
#------------------------------------------------#
function check_python_version()
{
    VERSION_FULL="$(${PYTHON_EXE} --version | awk '{ print $2 }' )"

    VERSION_MAJOR="$(echo ${VERSION_FULL} | sed 's/\./ /g' | awk '{ print $1 }' )"
    VERSION_MINOR="$(echo ${VERSION_FULL} | sed 's/\./ /g' | awk '{ print $2 }' )"

    if [ "${VERSION_MINOR}" -lt '11' ]; then
        echo "Python version cannot be less than 11. Actual version: ${VERSION_FULL}"
        exit 1
    fi
}

#  Check python
check_python_version

#  Check if venv already exists
if [ -d "${VENV_PATH}" ]; then
    echo "warning: Virtual-Environment already exists at ${VENV_PATH}"
    exit 1
fi

#  Create environment
${PYTHON_EXE} -m venv ${VENV_PATH}

#  Activate environment
. ${VENV_PATH}/bin/activate

#  Install updates
pip install --upgrade pip
