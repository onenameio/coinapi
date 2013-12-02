import json
import requests
import traceback
import time
from flask import render_template, Response, request, jsonify, abort

from coinvibes import app
from coinvibes.exchange_apis import get_exchange_api, get_exchange_api_tickers,\
	EXCHANGE_APIS
from coinvibes.utils import APIError, identify_user
from coinvibes.settings import RESOURCES, CURRENCY_PAIRS

import analytics

@app.route('/api/v1')
@identify_user
def api_index():
	analytics.track(request.remote_addr, 'API: entrypoint', {})

	data = {
		'resources': [
			{'name': 'Tickers', 'url': '/api/tickers' }
		 ]
	}

	return jsonify(data), 200

@app.route('/api/v1/tickers')
@identify_user
def all_tickers():
	analytics.track(request.remote_addr, 'API: all tickers', {
	})

	data = { 'exchanges': [] }

	for exchange_api in EXCHANGE_APIS:
		data['exchanges'].append(get_exchange_api_tickers(exchange_api))

	return jsonify(data), 200

@app.route('/api/v1/tickers/<exchange_slug>')
@identify_user
def all_currency_pairs_on_exchange(exchange_slug):
	analytics.track(request.remote_addr, 'API: exchange tickers', {
		'exchange': exchange_slug,
	})

	exchange_api = get_exchange_api(exchange_slug, EXCHANGE_APIS)
	if not exchange_api:
		abort(404)

	data = get_exchange_api_tickers(exchange_api)

	return jsonify(data), 200

@app.route('/api/v1/tickers/<exchange_slug>/<quote_currency>_<base_currency>')
@identify_user
def currency_pair_on_exchange(exchange_slug, quote_currency, base_currency):
	analytics.track(request.remote_addr, 'API: currency pair ticker', {
		'exchange': exchange_slug,
		'quote_currency': quote_currency,
		'base_currency': base_currency
	})

	exchange_api = get_exchange_api(exchange_slug, EXCHANGE_APIS)
	if not exchange_api:
		abort(404)

	try:
		data = exchange_api.ticker(quote_currency, base_currency)
	except:
		traceback.print_exc()
		return jsonify({'error': 'There seems to be a problem with the exchange API.'}), 500

	if data:
		data['coinvibes_timestamp'] = int(time.time())
		return jsonify(data), 200
	else:
		return jsonify({'error': 'did not get a proper response'}), 500


