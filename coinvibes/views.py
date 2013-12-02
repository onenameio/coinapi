import json
import requests
import traceback
import time
from flask import render_template, Response, request, jsonify, abort

from coinvibes import app
from coinvibes.exchange_apis import MtGoxAPI, BTCeAPI, BitstampAPI, KrakenAPI, \
	BTCChinaAPI, BitfinexAPI, CoinbaseAPI, get_exchange_api, \
	get_exchange_api_tickers, EXCHANGE_APIS
from coinvibes.utils import APIError
from coinvibes.settings import RESOURCES, CURRENCY_PAIRS

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/resources')
def resources():
	return render_template('resources.html', resources=RESOURCES)

@app.route('/exchanges')
def exchanges():
	return render_template('exchanges.html', exchanges=EXCHANGE_APIS)


@app.route('/currency-pairs')
def currency_pairs():
	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=CURRENCY_PAIRS)

@app.route('/btc-fiat-currency-pairs')
def bitcoin_fiat_pairs():
	currency_pairs = []
	for currency_pair in CURRENCY_PAIRS:
		if currency_pair['symbols'][0] == 'btc':
			currency_pairs.append(currency_pair)

	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=currency_pairs)

@app.route('/cryptocurrency-usd-currency-pairs')
def cryptocurrency_usd_pairs():
	currency_pairs = []
	for currency_pair in CURRENCY_PAIRS:
		if currency_pair['symbols'][1] == 'usd':
			currency_pairs.append(currency_pair)

	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=currency_pairs)

@app.route('/cryptocurrency-btc-currency-pairs')
def cryptocurrency_bitcoin_pairs():
	currency_pairs = []
	for currency_pair in CURRENCY_PAIRS:
		if currency_pair['symbols'][1] == 'btc':
			currency_pairs.append(currency_pair)

	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=currency_pairs)

@app.route('/')
def index():
	return render_template('index.html', exchanges=EXCHANGE_APIS)

# error handling
@app.errorhandler(APIError)
def handle_api_error(error):
	traceback.print_exc()
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

