DATE=`date +%Y-%m-%d`
curl -o correlation.png https://net-src.herokuapp.com/correlation.png
curl -o correlation.csv https://net-src.herokuapp.com/correlation.csv
curl -o rankings.csv https://net-src.herokuapp.com/ranking.csv

mv correlation.png correlation_${DATE}.png
mv correlation.csv correlation_${DATE}.csv
mv rankings.csv rankings_${DATE}.csv
