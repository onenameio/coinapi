import json
import requests
import traceback
import time
from flask import render_template, Response, request, jsonify, abort

from coinvibes import app
from coinvibes.exchange_apis import EXCHANGE_APIS
from coinvibes.utils import APIError, identify_user
from coinvibes.settings import RESOURCES, CURRENCY_PAIRS

import analytics

@app.route('/about')
@identify_user
def about():
	analytics.track(request.remote_addr, 'about page', {
	})
	return render_template('about.html')

@app.route('/resources')
@identify_user
def resources():
	analytics.track(request.remote_addr, 'resources page', {
	})
	return render_template('resources.html', resources=RESOURCES)

@app.route('/exchanges')
@identify_user
def exchanges():
	analytics.track(request.remote_addr, 'docs page', {
		'data': 'exchanges'
	})
	return render_template('exchanges.html', exchanges=EXCHANGE_APIS)

@app.route('/currency-pairs')
@identify_user
def currency_pairs():
	analytics.track(request.remote_addr, 'docs page', {
		'data': 'currency pairs'
	})
	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=CURRENCY_PAIRS)

@app.route('/btc-fiat-currency-pairs')
@identify_user
def bitcoin_fiat_pairs():
	analytics.track(request.remote_addr, 'docs page', {
		'data': 'btc/fiat currency pairs'
	})
	currency_pairs = []
	for currency_pair in CURRENCY_PAIRS:
		if currency_pair['symbols'][0] == 'btc':
			currency_pairs.append(currency_pair)

	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=currency_pairs)

@app.route('/cryptocurrency-usd-currency-pairs')
@identify_user
def cryptocurrency_usd_pairs():
	analytics.track(request.remote_addr, 'docs page', {
		'data': 'cryptocurrency/usd currency pairs'
	})
	currency_pairs = []
	for currency_pair in CURRENCY_PAIRS:
		if currency_pair['symbols'][1] == 'usd':
			currency_pairs.append(currency_pair)

	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=currency_pairs)

@app.route('/cryptocurrency-btc-currency-pairs')
@identify_user
def cryptocurrency_bitcoin_pairs():
	analytics.track(request.remote_addr, 'docs page', {
		'data': 'cryptocurrency/btc currency pairs'
	})
	currency_pairs = []
	for currency_pair in CURRENCY_PAIRS:
		if currency_pair['symbols'][1] == 'btc':
			currency_pairs.append(currency_pair)

	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=currency_pairs)

@app.route('/')
@identify_user
def index():
	analytics.track(request.remote_addr, 'home page', {
	})
	return render_template('index.html', exchanges=EXCHANGE_APIS)

# error handling
@app.errorhandler(APIError)
def handle_api_error(error):
	traceback.print_exc()
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

