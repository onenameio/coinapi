import json
import requests
import traceback
from flask import render_template, Response, request, jsonify, abort

from api import app
from api.exchange_apis import MtGoxAPI, BTCeAPI, BitstampAPI, KrakenAPI, \
	BTCChinaAPI, BitfinexAPI, get_exchange_api, get_exchange_api_tickers
from api.utils import APIError
from api.settings import RESOURCES, CURRENCY_PAIRS

EXCHANGE_APIS = [
	BitstampAPI(), MtGoxAPI(), BTCeAPI(), KrakenAPI(), BTCChinaAPI(),
	BitfinexAPI()
]

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/resources')
def resources():
	return render_template('resources.html', resources=RESOURCES)

@app.route('/exchanges')
def exchanges():
	return render_template('exchanges.html', exchanges=EXCHANGE_APIS)

@app.route('/currencies')
def currencies():
	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=CURRENCY_PAIRS)

@app.route('/')
def index():
	return render_template('index.html', exchanges=EXCHANGE_APIS)

@app.route('/api')
def api_index():
	data = {
		'resources': [
			{'name': 'Tickers', 'url': '/api/tickers' }
		 ]
	}

	return jsonify(data), 200

@app.route('/api/tickers')
def all_tickers():
	data = { 'exchanges': [] }

	for exchange_api in EXCHANGE_APIS:
		data['exchanges'].append(get_exchange_api_tickers(exchange_api))

	return jsonify(data), 200

@app.route('/api/tickers/<exchange_slug>')
def all_currency_pairs_on_exchange(exchange_slug):
	exchange_api = get_exchange_api(exchange_slug, EXCHANGE_APIS)
	if not exchange_api:
		abort(404)

	data = get_exchange_api_tickers(exchange_api)

	return jsonify(data), 200

@app.route('/api/tickers/<exchange_slug>/<quote_currency>_<base_currency>')
def currency_pair_on_exchange(exchange_slug, quote_currency, base_currency):
	exchange_api = get_exchange_api(exchange_slug, EXCHANGE_APIS)
	if not exchange_api:
		abort(404)

	try:
		data = exchange_api.ticker(quote_currency, base_currency)
	except:
		traceback.print_exc()
		return jsonify({'error': 'There seems to be a problem with the exchange API.'}), 500

	if data:
		return jsonify(data), 200
	else:
		return jsonify({'error': 'did not get a proper response'}), 500

# error handling
@app.errorhandler(APIError)
def handle_api_error(error):
	traceback.print_exc()
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

