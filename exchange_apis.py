import json
import requests
from flask import abort

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
		self.name = 'Mt. Gox'
		self.slug = 'mtgox'
		self.BASE_URL = 'http://data.mtgox.com/api/2'
		self.TICKER_ENDPOINTS = {
			('btc', 'usd'): '/BTCUSD/money/ticker'
		}

	def ticker(self, target_currency, native_currency):
		ticker_data = self.ticker_data(target_currency, native_currency)['data']

		ticker = {
			'price_units': native_currency,
			'vol': float(ticker_data['vol']['value_int']),
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
		self.name = 'BTC-e'
		self.slug = 'btce'
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
			'vol': float(ticker_data['vol']),
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
		self.name = 'Bitstamp'
		self.slug = 'bitstamp'
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

class KrakenAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'Kraken'
		self.slug = 'kraken'
		self.BASE_URL = 'https://api.kraken.com/0/public'
		self.TICKER_ENDPOINTS = {
			('btc', 'usd'): '/Ticker?pair=XXBTZUSD',
			('nmc', 'usd'): '/Ticker?pair=XNMCZUSD',
			('ltc', 'usd'): '/Ticker?pair=XLTCZUSD',
			('btc', 'nmc'): '/Ticker?pair=XXBTXNMC',
		}

	def ticker(self, target_currency, native_currency):
		ticker_data = self.ticker_data(target_currency, native_currency)

		endpoint_name = self.TICKER_ENDPOINTS.get((target_currency, native_currency))
		pair_name = endpoint_name.strip('/Ticker?pair=')
		ticker_data = ticker_data['result'][pair_name]

		ticker = {
			'price_units': native_currency,
			'volume': self.float_price(ticker_data['v'][0]),
			'bid': self.float_price(ticker_data['b'][0]),
			'ask': self.float_price(ticker_data['a'][0]),
			'high': self.float_price(ticker_data['h'][0]),
			'low': self.float_price(ticker_data['l'][0]),			
			'average': self.float_price(ticker_data['p'][0]),
		}

		return ticker

class BTCChinaAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'BTC China'
		self.slug = 'btcchina'
		self.BASE_URL = 'https://vip.btcchina.com'
		self.TICKER_ENDPOINTS = {
			('btc', 'cny'): '/bc/ticker',
		}

	def ticker(self, target_currency, native_currency):
		ticker_data = self.ticker_data(target_currency, native_currency)['ticker']

		ticker = {
			'price_units': native_currency,
			'vol': float(ticker_data['vol']),
			'bid': self.float_price(ticker_data['buy']),
			'ask': self.float_price(ticker_data['sell']),
			'high': self.float_price(ticker_data['high']),
			'low': self.float_price(ticker_data['low']),
			'last': self.float_price(ticker_data['last']),
		}

		return ticker

class BitfinexAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'Bitfinex'
		self.slug = 'bitfinex'
		self.BASE_URL = 'https://api.bitfinex.com/v1'
		self.TICKER_ENDPOINTS = {
			('btc', 'usd'): '/ticker/btcusd',
			('ltc', 'usd'): '/ticker/ltcusd',
			('ltc', 'btc'): '/ticker/ltcbtc',
		}

	def ticker(self, target_currency, native_currency):
		ticker_data = self.ticker_data(target_currency, native_currency)

		ticker = {
			'price_units': native_currency,
			'bid': self.float_price(ticker_data['bid']),
			'ask': self.float_price(ticker_data['ask']),
			'last': self.float_price(ticker_data['last_price']),
			'timestamp': int(float(ticker_data['timestamp'])),
		}

		return ticker

