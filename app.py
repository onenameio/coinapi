import json
import requests
import traceback
from flask import Flask, render_template, Response, request, jsonify, abort
from exchange_apis import MtGoxAPI, BTCeAPI, BitstampAPI, KrakenAPI, \
	BTCChinaAPI, BitfinexAPI

app = Flask(__name__)
app.config.from_object('settings')

EXCHANGE_APIS = [
	BitstampAPI(), MtGoxAPI(), BTCeAPI(), KrakenAPI(), BTCChinaAPI(),
	BitfinexAPI()
]

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/exchanges')
def exchanges():
	return render_template('exchanges.html', exchanges=EXCHANGE_APIS)

@app.route('/currencies')
def currencies():
	currency_pairs = [
		{ 'name': 'Bitcoin / US Dollars', 'symbols': ('btc','usd') },
		{ 'name': 'Bitcoin / Chinese Yuan', 'symbols': ('btc','cny') },
		{ 'name': 'Litecoin / US Dollars', 'symbols': ('ltc','usd') },
		{ 'name': 'Litecoin / Bitcoin', 'symbols': ('ltc','btc') },
		{ 'name': 'Namecoin / US Dollars', 'symbols': ('nmc','usd') },
		{ 'name': 'Namecoin / Bitcoin', 'symbols': ('nmc','btc') },
		{ 'name': 'Peercoin / Bitcoin', 'symbols': ('ppc','btc') },
		{ 'name': 'Primecoin / Bitcoin', 'symbols': ('xpm','btc') },
		#{ 'name': 'Novacoin / Bitcoin', 'symbols': ('nvc','btc') },
		#{ 'name': 'Terracoin / Bitcoin', 'symbols': ('trc','btc') },
	]
	return render_template('currencies.html', exchanges=EXCHANGE_APIS,
						   currency_pairs=currency_pairs)

@app.route('/')
def index():
	return render_template('index.html', exchanges=EXCHANGE_APIS)

"""@app.route('/tickers/<target_currency>_<native_currency>')
def all_exchanges(target_currency, native_currency):
	data = {}
	
	for exchange in EXCHANGE_APIS:
		exchange_data = exchange.ticker(target_currency, native_currency)
		data[exchange.slug] = exchange_data

	return jsonify(data), 200"""

@app.route('/api/tickers/<exchange>/<target_currency>_<native_currency>')
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
	elif exchange == 'bitfinex':
		exchange_api = BitfinexAPI()
	else:
		abort(404)

	data = exchange_api.ticker(target_currency, native_currency)

	if data:
		return jsonify(data), 200
	else:
		return jsonify({'error': 'did not get a proper response'}), 500

@app.errorhandler(Exception)
def basic_error_handler(e):
	traceback.print_exc()
	return jsonify({'error': 'there was a problem with the server'}), 500



# just for testing
@app.route('/help')
def help():
	return render_template('help.html')

@app.route('/tree')
def tree():
	return render_template('tree.html')

@app.route('/content')
def content():
	return render_template('content.html')

