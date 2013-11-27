import json
import requests
from flask import Flask, render_template, Response, request, jsonify, abort
from exchange_apis import MtGoxAPI, BTCeAPI, BitstampAPI, KrakenAPI, BTCChinaAPI

app = Flask(__name__)
app.config.from_object('settings')

EXCHANGE_APIS = [MtGoxAPI(), BTCeAPI(), BitstampAPI(), KrakenAPI(), BTCChinaAPI()]

@app.route('/')
def index():
	return render_template('index.html', exchanges=EXCHANGE_APIS)

@app.route('/tickers/<target_currency>_<native_currency>')
def all_exchanges(target_currency, native_currency):
	data = {}
	
	for exchange in EXCHANGE_APIS:
		exchange_data = exchange.ticker(target_currency, native_currency)
		data[exchange.slug] = exchange_data

	return jsonify(data), 200

@app.route('/tickers/<exchange>/<target_currency>_<native_currency>')
def single_exchange(exchange, target_currency, native_currency):
	if exchange == 'mtgox':
		exchange_api = MtGoxAPI()
	elif exchange == 'btce':
		exchange_api = BTCeAPI()
	elif exchange == 'bitstamp':
		exchange_api = BitstampAPI()
	elif exchange == 'kraken':
		exchange_api = KrakenAPI()
	elif exchange == 'btcchina':
		exchange_api = BTCChinaAPI()
	else:
		abort(404)

	data = exchange_api.ticker(target_currency, native_currency)

	if data:
		return jsonify(data), 200
	else:
		return jsonify({'error': 'did not get a proper response'}), 500

@app.errorhandler(Exception)
def basic_error_handler(e):
	return jsonify({'error': 'there was a problem with the server'}), 500

