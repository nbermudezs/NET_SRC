#!/usr/bin/env bash

# make sure to set the NET_SRC_HOME env variable by doing
# export NET_SRC_HOME=~/somepath

# also set the env variable DAILY_DATA
# i.e. export DAILY_DATA=/home/nbermudezs/cron/net_src/

cd ${NET_SRC_HOME}
python -m utils.trendline ${DAILY_DATA}