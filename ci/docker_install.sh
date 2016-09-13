#!/bin/bash

[[ ! -e /.dockerenv ]] && [[ ! -e /.dockerinit ]] && exit 0
apt-get update -yqq
apt-get install -yqq git python3 python3-dev python3-pip wget
