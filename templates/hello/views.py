import base64
import io
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import date
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import render_template, Blueprint, make_response, send_file, jsonify, request
from utils.analyzer import Analyzer

plt.rcParams['figure.dpi'] = 300

hello_blueprint = Blueprint('hello',__name__)

from templates.hello.collect_data import collect_rankings

rankings = collect_rankings()
last_updated = date.today()
POWER_SEVEN_CONFS = ['Big Ten', 'Big 12', 'Pac-12', 'ACC', 'American', 'SEC', 'Big East']


def prepare_rankings(all_ranks):
	conf_ranks = all_ranks.groupby('Conf')
	conf_ranks = {conf: df for conf, df in conf_ranks}

	conf = request.args.get('conf')
	if conf is None:
		return all_ranks.copy()
	if conf == 'PowerSeven':
		teams = pd.concat([conf_ranks[team] for team in POWER_SEVEN_CONFS])
		teams = teams.sort_values(by='RPI - NET', ascending=True)
		return teams
	if conf == 'Others':
		teams = pd.concat([df for conf, df in conf_ranks.items()
						   if conf not in POWER_SEVEN_CONFS])
		teams = teams.sort_values(by='RPI - NET', ascending=True)
		return teams
	return conf_ranks[conf]


@hello_blueprint.route('/')
@hello_blueprint.route('/hello')
def index():
	return render_template("index.html")


@hello_blueprint.route('/ranking.json')
def data():
	global rankings, last_updated
	si = io.StringIO()
	if rankings is None or (date.today() - last_updated).days > 0:
		rankings = collect_rankings()
		last_updated = date.today()

	tmp_rankings = prepare_rankings(rankings)
	tmp_rankings.to_json(si, orient='index')

	output = make_response(si.getvalue())
	output.headers["Content-Type"] = "application/json"
	output.cache_control.max_age = 60 * 60 * 24

	return output


@hello_blueprint.route('/ranking.csv')
def data_csv():
	global rankings, last_updated
	si = io.StringIO()
	if rankings is None or (date.today() - last_updated).days > 0:
		rankings = collect_rankings()
		last_updated = date.today()
	tmp_rankings = prepare_rankings(rankings)
	tmp_rankings.to_csv(si)

	output = make_response(si.getvalue())
	output.headers["Content-Disposition"] = "attachment; filename=rankings.csv"
	output.headers["Content-Type"] = "text/csv"
	output.cache_control.max_age = 60 * 60 * 24
	return output


@hello_blueprint.route('/correlation.json')
def correlation_json():
	global rankings, last_updated
	si = io.StringIO()
	if rankings is None or (date.today() - last_updated).days > 0:
		rankings = collect_rankings()
		last_updated = date.today()

	tmp_rankings = prepare_rankings(rankings)
	tmp_rankings = tmp_rankings.drop(['RPI - NET', 'Conf'], axis=1)
	tmp_rankings.corr(method='spearman').round(3).to_json(si, orient='index')

	output = make_response(si.getvalue())
	output.headers["Content-Type"] = "application/json"
	output.cache_control.max_age = 60 * 60 * 24

	return output


@hello_blueprint.route('/correlation.png')
def correlation_png():
	global rankings, last_updated
	img = io.BytesIO()
	if rankings is None or (date.today() - last_updated).days > 0:
		rankings = collect_rankings()
		last_updated = date.today()

	tmp_rankings = prepare_rankings(rankings)

	tmp_rankings['Sagarin'] = tmp_rankings['Sagarin_RK']
	tmp_rankings['KenPom'] = tmp_rankings['Pomeroy_RK']
	tmp_rankings['BPI'] = tmp_rankings['BPI_RK']
	tmp_rankings['NET'] = tmp_rankings['NET Rank']

	fig = sns.pairplot(tmp_rankings,
					   y_vars=['KenPom', 'BPI', 'RPI', 'NET'],
					   x_vars=['Sagarin', 'KenPom', 'BPI', 'RPI'],
					   # kind='reg',
					   plot_kws={'color': 'black'})
	fig.set(ylim=(0, 380), xlim=(0, 380))
	for i, j in zip(*np.triu_indices_from(fig.axes, 1)):
		fig.axes[i, j].set_visible(False)
	FigureCanvas(fig.fig).print_png(img)

	output = make_response(img.getvalue())
	output.headers["Content-Disposition"] = "inline"
	output.headers["Content-Type"] = "image/png"
	output.cache_control.max_age = 60 * 60 * 24

	return output


@hello_blueprint.route('/correlationByConf.png')
def correlation_by_conf_png():
	global rankings, last_updated
	img = io.BytesIO()
	if rankings is None or (date.today() - last_updated).days > 0:
		rankings = collect_rankings()
		last_updated = date.today()

	tmp_rankings = prepare_rankings(rankings)

	tmp_rankings['Sagarin'] = tmp_rankings['Sagarin_RK']
	tmp_rankings['KenPom'] = tmp_rankings['Pomeroy_RK']
	tmp_rankings['BPI'] = tmp_rankings['BPI_RK']
	tmp_rankings['NET'] = tmp_rankings['NET Rank']
	tmp_rankings['Conference'] = tmp_rankings['Conf']

	n = request.args.get('n', '8')

	if n == '8':
		tmp_rankings['Conference'][tmp_rankings['Conference'].isin(POWER_SEVEN_CONFS) == False] = 'Other'
		fig = sns.pairplot(tmp_rankings,
						   y_vars=['KenPom', 'BPI', 'RPI', 'NET'],
						   x_vars=['Sagarin', 'KenPom', 'BPI', 'RPI'],
						   hue='Conference',
						   hue_order=['American', 'ACC', 'Big 12', 'Big East', 'Big Ten', 'Pac-12', 'SEC', 'Other'],
						   markers=['p', 's', 'x', 'H', 'o', 'P', 'D', '*'],
						   plot_kws=dict(alpha=0.8))
	elif n == '2':
		tmp_rankings['Conference'][tmp_rankings['Conference'].isin(POWER_SEVEN_CONFS) == False] = 'Other'
		tmp_rankings['Conference'][tmp_rankings['Conference'].isin(POWER_SEVEN_CONFS)] = 'Power 7'
		fig = sns.pairplot(tmp_rankings,
						   y_vars=['KenPom', 'BPI', 'RPI', 'NET'],
						   x_vars=['Sagarin', 'KenPom', 'BPI', 'RPI'],
						   hue='Conference',
						   hue_order=['Power 7', 'Other'],
						   markers=['s', 'o'],
						   plot_kws=dict(alpha=0.5, color='black'))
	elif n == 'all':
		fig = sns.pairplot(tmp_rankings,
						   y_vars=['KenPom', 'BPI', 'RPI', 'NET'],
						   x_vars=['Sagarin', 'KenPom', 'BPI', 'RPI'],
						   hue='Conference',
						   plot_kws=dict(alpha=0.8))
	fig.set(ylim=(0, 380), xlim=(0, 380))
	for i, j in zip(*np.triu_indices_from(fig.axes, 1)):
		fig.axes[i, j].set_visible(False)
	FigureCanvas(fig.fig).print_png(img)

	output = make_response(img.getvalue())
	output.headers["Content-Disposition"] = "inline"
	output.headers["Content-Type"] = "image/png"
	output.cache_control.max_age = 60 * 60 * 24

	return output


@hello_blueprint.route('/correlation.csv')
def correlation_csv():
	global rankings, last_updated
	si = io.StringIO()
	if rankings is None or (date.today() - last_updated).days > 0:
		rankings = collect_rankings()
		last_updated = date.today()

	tmp_rankings = prepare_rankings(rankings)
	tmp_rankings = tmp_rankings.drop(['RPI - NET', 'Conf'], axis=1)
	tmp_rankings.corr(method='spearman').to_csv(si)

	output = make_response(si.getvalue())
	output.headers["Content-Disposition"] = "attachment; filename=corr.csv"
	output.headers["Content-Type"] = "text/csv"
	output.cache_control.max_age = 60 * 60 * 24
	return output


@hello_blueprint.route('/correlation.txt')
def correlation_txt():
	global rankings, last_updated
	with open('templates/output/as_html.txt') as f:
		template = f.read()

	if rankings is None or (date.today() - last_updated).days > 0:
		rankings = collect_rankings()
		last_updated = date.today()

	tmp_rankings = prepare_rankings(rankings)
	tmp_rankings = tmp_rankings.drop(['RPI - NET', 'Conf'], axis=1)
	corr = tmp_rankings.corr(method='spearman')
	payload = template.format(
		date=date.today().strftime('%d %B %Y'),
		sagarinVpomeroy=corr['Sagarin_RK']['Pomeroy_RK'].round(3),
		sagarinVrpi=corr['Sagarin_RK']['RPI'].round(3),
		sagarinVbpi=corr['Sagarin_RK']['BPI_RK'].round(3),
		sagarinVnet=corr['Sagarin_RK']['NET Rank'].round(3),
		pomeroyVrpi=corr['Pomeroy_RK']['RPI'].round(3),
		pomeroyVbpi=corr['Pomeroy_RK']['BPI_RK'].round(3),
		pomeroyVnet=corr['Pomeroy_RK']['NET Rank'].round(3),
		rpiVbpi=corr['RPI']['BPI_RK'].round(3),
		rpiVnet=corr['RPI']['NET Rank'].round(3),
		bpiVnet=corr['BPI_RK']['NET Rank'].round(3)
	)

	output = make_response(payload)
	output.headers["Content-Disposition"] = "attachment; filename=corr.txt"
	output.headers["Content-Type"] = "text/plain; charset=utf-8"
	output.cache_control.max_age = 60 * 60 * 24
	return output


@hello_blueprint.route('/outliers.json')
def outliers_json():
	global rankings, last_updated

	analyzer = Analyzer()
	if rankings is None or (date.today() - last_updated).days > 0:
		rankings = collect_rankings()
		last_updated = date.today()

	tmp_rankings = prepare_rankings(rankings)
	tmp_rankings = tmp_rankings.drop(['RPI - NET', 'Conf'], axis=1)
	corr = tmp_rankings.corr(method='spearman')
	outliers = analyzer.get_outliers(tmp_rankings, corr)
	return jsonify(outliers)
