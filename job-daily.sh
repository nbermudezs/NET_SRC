#!/usr/bin/env bash

export DATA_HOME='REPLACE_ME'
export SENDGRID_TO_DEVELOPER='REPLACE_ME'
export SENDGRID_FROM='REPLACE_ME'
export SENDGRID_API_KEY='REPLACE_ME'

curl -o ${DATA_HOME}/correlation.png https://net-src.herokuapp.com/correlation.png
sleep 60

DATE=`date +%Y-%m-%d`
curl -o ${DATA_HOME}/correlation_${DATE}.png https://net-src.herokuapp.com/correlation.png
curl -o ${DATA_HOME}/correlation_PowerSeven_${DATE}.png https://net-src.herokuapp.com/correlation.png?conf=PowerSeven
curl -o ${DATA_HOME}/correlation_Others_${DATE}.png https://net-src.herokuapp.com/correlation.png?conf=Others
curl -o ${DATA_HOME}/correlation_${DATE}.csv https://net-src.herokuapp.com/correlation.csv
curl -o ${DATA_HOME}/correlation_PowerSeven_${DATE}.csv https://net-src.herokuapp.com/correlation.csv?conf=PowerSeven
curl -o ${DATA_HOME}/correlation_Others_${DATE}.csv https://net-src.herokuapp.com/correlation.csv?conf=Others
curl -o ${DATA_HOME}/correlation_${DATE}.txt https://net-src.herokuapp.com/correlation.txt
curl -o ${DATA_HOME}/rankings_${DATE}.csv https://net-src.herokuapp.com/ranking.csv
curl -o ${DATA_HOME}/rankings_PowerSeven_${DATE}.csv https://net-src.herokuapp.com/ranking.csv?conf=PowerSeven
curl -o ${DATA_HOME}/rankings_Others_${DATE}.csv https://net-src.herokuapp.com/ranking.csv?conf=Others
curl -o ${DATA_HOME}/KPvNET_rankings_${DATE}.csv https://net-src.herokuapp.com/ranking.csv&sort=KPvNET
curl -o ${DATA_HOME}/KPvNET_rankings_PowerSeven_${DATE}.csv https://net-src.herokuapp.com/ranking.csv?conf=PowerSeven&sort=KPvNET
curl -o ${DATA_HOME}/KPvNET_rankings_Others_${DATE}.csv https://net-src.herokuapp.com/ranking.csv?conf=Others&sort=KPvNET
curl -o ${DATA_HOME}/outliers_${DATE}.json https://net-src.herokuapp.com/outliers.json
curl -o ${DATA_HOME}/net-v-all.png https://net-src.herokuapp.com/net-v-all.png

cd ${NET_SRC_HOME}
/usr/bin/python3 -m utils.error_notifier ${DATA_HOME}/rankings_${DATE}.csv