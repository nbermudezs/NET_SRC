import base64
import io
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import date
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import render_template, Blueprint, make_response, send_file, jsonify
from utils.analyzer import Analyzer

plt.rcParams['figure.dpi'] = 300

hello_blueprint = Blueprint('hello',__name__)

from templates.hello.collect_data import collect_rankings

rankings = collect_rankings()
last_updated = date.today()

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
	result = rankings.to_json(si, orient='index')

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
	rankings.to_csv(si)

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
	result = rankings.corr(method='spearman').round(3).to_json(si, orient='index')

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
	rankings['Sagarin'] = rankings['Sagarin_RK']
	rankings['KenPom'] = rankings['Pomeroy_RK']
	rankings['BPI'] = rankings['BPI_RK']
	rankings['NET'] = rankings['NET Rank']

	fig = sns.pairplot(rankings,
					   y_vars=['KenPom', 'BPI', 'RPI', 'NET'],
					   x_vars=['Sagarin', 'KenPom', 'BPI', 'RPI'],
					   kind='reg',
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


@hello_blueprint.route('/correlation.csv')
def correlation_csv():
	global rankings, last_updated
	si = io.StringIO()
	if rankings is None or (date.today() - last_updated).days > 0:
		rankings = collect_rankings()
		last_updated = date.today()

	rankings.corr(method='spearman').to_csv(si)

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

	corr = rankings.corr(method='spearman')
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

	corr = rankings.corr(method='spearman')
	outliers = analyzer.get_outliers(rankings, corr)
	return jsonify(outliers)
