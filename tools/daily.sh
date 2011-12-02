#!/bin/sh

env_root=$1
manage_root=$2
settings=$3

source "$env_root/bin/activate"
cd ..
"$manage_root"/manage.py openportfolio-daily --settings="$settings"
