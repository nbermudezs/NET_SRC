import base64
import io
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import render_template, Blueprint, make_response, send_file

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
	result = rankings.corr(method='spearman').to_json(si, orient='index')

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
	fig = sns.pairplot(rankings, vars=['Sagarin_RK', 'Pomeroy_RK', 'BPI_RK', 'RPI', 'NET Rank'])
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
