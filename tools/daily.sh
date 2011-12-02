#!/bin/sh

env_root=$1
settings=$2

source "$1/bin/activate"
cd ..
./manage.py openportfolio-daily --settings="$2"
