import json
import requests
from flask import Flask, render_template, Response, request, jsonify, abort

# initialization
app = Flask(__name__)
app.config.from_object('settings')

class ExchangeAPI(object):
	def __init__(self):
		raise NotImplementedError()

	def float_price(self, price):
		try:
			return float(str(price).strip('$'))
		except ValueError:
			return price

	def ticker_data(self, target_currency, native_currency):
		ticker_endpoint = self.TICKER_ENDPOINTS.get((target_currency, native_currency))
		if ticker_endpoint:
			r = requests.get(self.BASE_URL + ticker_endpoint)
		else:
			abort(404)
		
		try:
			data = json.loads(r.text)
		except ValueError:
			data = None
		
		return data

class MtGoxAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'mtgox'
		self.BASE_URL = 'http://data.mtgox.com/api/2'
		self.TICKER_ENDPOINTS = {
			('btc', 'usd'): '/BTCUSD/money/ticker'
		}

	def ticker(self, target_currency, native_currency):
		ticker_data = self.ticker_data(target_currency, native_currency)['data']

		ticker = {
			'price_units': native_currency,
			'volume': float(ticker_data['vol']['value_int']),
			'bid': self.float_price(ticker_data['buy']['display']),
			'ask': self.float_price(ticker_data['sell']['display']),
			'high': self.float_price(ticker_data['high']['display']),
			'low': self.float_price(ticker_data['low']['display']),
			'timestamp': int(ticker_data['now'])/(1000*1000),
			'last': self.float_price(ticker_data['last']['display']),
			'average': self.float_price(ticker_data['avg']['display']),
			'vwap': self.float_price(ticker_data['vwap']['display']),
		}

		return ticker

class BTCeAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'btce'
		self.BASE_URL = 'https://btc-e.com/api/2'
		self.TICKER_ENDPOINTS = {
			('btc', 'usd'): '/btc_usd/ticker',
			('ltc', 'usd'): '/ltc_usd/ticker',
			('ltc', 'btc'): '/ltc_btc/ticker',
			('nmc', 'btc'): '/nmc_btc/ticker',
			('ppc', 'btc'): '/ppc_btc/ticker',
			('xpm', 'btc'): '/xpm_btc/ticker',
			('nvc', 'btc'): '/nvc_btc/ticker',
			('trc', 'btc'): '/trc_btc/ticker',
		}

	def ticker(self, target_currency, native_currency):
		ticker_data = self.ticker_data(target_currency, native_currency)['ticker']

		ticker = {
			'price_units': native_currency,
			'volume': float(ticker_data['vol']),
			'bid': ticker_data['buy'],
			'ask': ticker_data['sell'],
			'high': ticker_data['high'],
			'low': ticker_data['low'],
			'timestamp': int(ticker_data['server_time']),
			'last': ticker_data['last'],
			'average': ticker_data['avg'],
		}

		return ticker

class BitstampAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'bitstamp'
		self.BASE_URL = 'https://www.bitstamp.net/api'
		self.TICKER_ENDPOINTS = {
			('btc', 'usd'): '/ticker/'
		}

	def ticker(self, target_currency, native_currency):
		ticker_data = self.ticker_data(target_currency, native_currency)

		ticker = {
			'price_units': native_currency,
			'volume': float(ticker_data['volume']),
			'bid': self.float_price(ticker_data['bid']),
			'ask': self.float_price(ticker_data['ask']),
			'high': self.float_price(ticker_data['high']),
			'low': self.float_price(ticker_data['low']),
			'timestamp': int(ticker_data['timestamp']),
		}

		return ticker

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/tickers/<target_currency>_<native_currency>')
def all_exchanges(target_currency, native_currency):
	data = {}
	exchanges = [MtGoxAPI(), BTCeAPI(), BitstampAPI()]
	for exchange in exchanges:
		exchange_data = exchange.ticker(target_currency, native_currency)
		data[exchange.name] = exchange_data

	return jsonify(data), 200

@app.route('/tickers/<exchange>/<target_currency>_<native_currency>')
def single_exchange(exchange, target_currency, native_currency):
	if exchange == 'mtgox':
		exchange_api = MtGoxAPI()
	elif exchange == 'btce':
		exchange_api = BTCeAPI()
	elif exchange == 'bitstamp':
		exchange_api = BitstampAPI()
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


