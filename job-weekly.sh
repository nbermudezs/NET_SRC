#!/usr/bin/env bash

# This script assumes that:
# 1. the entire repository is available under the /home/bracketodds/NET_SRC directory
# 2. there is a Python virtual environment under /home/bracketodds/python-venv
# 3. the files summarizing the weekly data will be stored in /home/bracketodds/cron/net_src/

source /home/bracketodds/python-venv/bin/activate
cd /home/bracketodds/NET_SRC
python -m utils.trendline /home/bracketodds/cron/net_src/
python -m utils.rpi_trendline /home/bracketodds/cron/net_src/

export DAILY_DATA='/home/bracketodds/cron/net_src/'
export SENDGRID_TO='REPLACE_ME'
export SENDGRID_FROM='REPLACE_ME'
export SENDGRID_TEMPLATE_ID='REPLACE_ME'
export SENDGRID_API_KEY='REPLACE_ME'
python -m utils.send_email ${DAILY_DATA}
