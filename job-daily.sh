#!/usr/bin/env bash
DATE=`date +%Y-%m-%d`
curl -o correlation.png https://net-src.herokuapp.com/correlation.png
curl -o correlation_PowerSeven_${DATE}.png https://net-src.herokuapp.com/correlation.png?conf=PowerSeven
curl -o correlation_Others_${DATE}.png https://net-src.herokuapp.com/correlation.png?conf=Others
curl -o correlation.csv https://net-src.herokuapp.com/correlation.csv
curl -o correlation_PowerSeven_${DATE}.csv https://net-src.herokuapp.com/correlation.csv?conf=PowerSeven
curl -o correlation_Others_${DATE}.csv https://net-src.herokuapp.com/correlation.csv?conf=Others
curl -o correlation.txt https://net-src.herokuapp.com/correlation.txt
curl -o rankings.csv https://net-src.herokuapp.com/ranking.csv
curl -o rankings_PowerSeven_${DATE}.csv https://net-src.herokuapp.com/ranking.csv?conf=PowerSeven
curl -o rankings_Others_${DATE}.csv https://net-src.herokuapp.com/ranking.csv?conf=Others
curl -o outliers.json https://net-src.herokuapp.com/outliers.json
curl -o net-v-all.png https://net-src.herokuapp.com/net-v-all.png

curl -o correlationByConf_A_${DATE}.png https://net-src.herokuapp.com/correlationByConf.png?n=8
curl -o correlationByConf_B_${DATE}.png https://net-src.herokuapp.com/correlation.png?n=2

mv correlation.png correlation_${DATE}.png
mv correlation.csv correlation_${DATE}.csv
mv correlation.txt correlation_${DATE}.txt
mv rankings.csv rankings_${DATE}.csv
mv outliers.json outliers_${DATE}.json
