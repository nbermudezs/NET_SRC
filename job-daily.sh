#!/usr/bin/env bash
DATE=`date +%Y-%m-%d`
curl -o correlation.png https://net-src.herokuapp.com/correlation.png
curl -o correlation.csv https://net-src.herokuapp.com/correlation.csv
curl -o correlation.txt https://net-src.herokuapp.com/correlation.txt
curl -o rankings.csv https://net-src.herokuapp.com/ranking.csv

mv correlation.png correlation_${DATE}.png
mv correlation.csv correlation_${DATE}.csv
mv correlation.txt correlation_${DATE}.txt
mv rankings.csv rankings_${DATE}.csv
