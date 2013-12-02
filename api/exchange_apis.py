import json
import requests
import traceback
from flask import abort
from api.utils import APIError, remove_non_ascii, remove_non_numeric

def get_exchange_api(exchange_slug, exchange_apis):
	for exchange_api in exchange_apis:
		if exchange_slug == exchange_api.slug:
			return exchange_api
	return None

def get_exchange_api_tickers(exchange_api):
	exchange_data = {
		'name': exchange_api.name,
		'slug': exchange_api.slug,
		'url': '/api/tickers/' + exchange_api.slug,
		'tickers': []
	}
	for ticker_key in exchange_api.tickers:
		ticker = exchange_api.tickers[ticker_key]
		ticker_data = {
			'quote_currency': ticker_key[0],
			'base_currency': ticker_key[1],
			'url': '/api/tickers/' + exchange_api.slug + '/' + ticker_key[0] + '_' + ticker_key[1]
		}
		exchange_data['tickers'].append(ticker_data)
	return exchange_data

def format_currency_string(s):
	pass

class ExchangeAPI(object):
	def __init__(self):
		raise NotImplementedError()

	def float_price(self, price):
		price_no_ascii = remove_non_ascii(price)
		price_numberified = remove_non_numeric(price_no_ascii)
		try:
			return float(price_numberified)
		except ValueError:
			traceback.print_exc()
			return price

	def ticker_data(self, quote_currency, base_currency):
		ticker = self.tickers.get((quote_currency, base_currency))
		if ticker:
			try:
				r = requests.get(self.base_url + ticker.get('url'),
								 timeout=4, verify=False)
			except requests.exceptions.Timeout:
				raise APIError('Timeout')
		else:
			abort(404)

		try:
			data = json.loads(r.text)
		except ValueError:
			traceback.print_exc()
			data = None
		
		return data

	def ticker(self, quote_currency, base_currency):
		raise NotImplementedError()

class MtGoxAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'Mt. Gox'
		self.slug = 'mtgox'
		self.base_url = 'http://data.mtgox.com/api/2'
		self.tickers = {
			('btc', 'usd'): { 'url': '/BTCUSD/money/ticker' },
			('btc', 'jpy'): { 'url': '/BTCJPY/money/ticker' },
			('btc', 'eur'): { 'url': '/BTCEUR/money/ticker' },
			('btc', 'cny'): { 'url': '/BTCCNY/money/ticker' },
			('btc', 'cad'): { 'url': '/BTCCAD/money/ticker' },
			('btc', 'aud'): { 'url': '/BTCAUD/money/ticker' },
			('btc', 'chf'): { 'url': '/BTCCHF/money/ticker' },
			('btc', 'dkk'): { 'url': '/BTCDKK/money/ticker' },
			('btc', 'gbp'): { 'url': '/BTCGBP/money/ticker' },
			('btc', 'hkd'): { 'url': '/BTCHKD/money/ticker' },
			('btc', 'nok'): { 'url': '/BTCNOK/money/ticker' },
			('btc', 'nzd'): { 'url': '/BTCNZD/money/ticker' },
			('btc', 'pln'): { 'url': '/BTCPLN/money/ticker' },
			('btc', 'rub'): { 'url': '/BTCRUB/money/ticker' },
			('btc', 'sek'): { 'url': '/BTCSEK/money/ticker' },
			('btc', 'sgd'): { 'url': '/BTCSGD/money/ticker' },
			('btc', 'thb'): { 'url': '/BTCTHB/money/ticker' },
		}

	def ticker(self, quote_currency, base_currency):
		ticker_data = self.ticker_data(quote_currency, base_currency)['data']

		ticker = {
			'price_units': base_currency,
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
		self.base_url = 'https://btc-e.com/api/2'
		self.tickers = {
			('btc', 'usd'): { 'url': '/btc_usd/ticker' },
			('btc', 'eur'): { 'url': '/btc_eur/ticker' },
			('ltc', 'usd'): { 'url': '/ltc_usd/ticker' },
			('ltc', 'eur'): { 'url': '/ltc_eur/ticker' },
			('ltc', 'btc'): { 'url': '/ltc_btc/ticker' },
			('nmc', 'btc'): { 'url': '/nmc_btc/ticker' },
			('ppc', 'btc'): { 'url': '/ppc_btc/ticker' },
			('xpm', 'btc'): { 'url': '/xpm_btc/ticker' },
			('nvc', 'btc'): { 'url': '/nvc_btc/ticker' },
			('trc', 'btc'): { 'url': '/trc_btc/ticker' },
		}

	def ticker(self, quote_currency, base_currency):
		ticker_data = self.ticker_data(quote_currency, base_currency)['ticker']

		ticker = {
			'price_units': base_currency,
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
		self.base_url = 'https://www.bitstamp.net/api'
		self.tickers = {
			('btc', 'usd'): { 'url': '/ticker/' }
		}

	def ticker(self, quote_currency, base_currency):
		ticker_data = self.ticker_data(quote_currency, base_currency)

		ticker = {
			'price_units': base_currency,
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
		self.base_url = 'https://api.kraken.com/0/public'
		self.tickers = {
			('btc', 'usd'): { 'url': '/Ticker?pair=XXBTZUSD' },
			('btc', 'eur'): { 'url': '/Ticker?pair=XXBTZEUR' },
			('nmc', 'usd'): { 'url': '/Ticker?pair=XNMCZUSD' },
			('nmc', 'eur'): { 'url': '/Ticker?pair=XNMCZEUR' },
			('ltc', 'usd'): { 'url': '/Ticker?pair=XLTCZUSD' },
			('ltc', 'eur'): { 'url': '/Ticker?pair=XLTCZEUR' },
			('btc', 'nmc'): { 'url': '/Ticker?pair=XXBTXNMC' },
		}

	def ticker(self, quote_currency, base_currency):
		ticker_data = self.ticker_data(quote_currency, base_currency)

		ticker = self.tickers.get((quote_currency, base_currency))
		pair_name = ticker.get('url').strip('/Ticker?pair=')
		ticker_data = ticker_data['result'][pair_name]

		ticker = {
			'price_units': base_currency,
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
		self.base_url = 'https://vip.btcchina.com'
		self.tickers = {
			('btc', 'cny'): { 'url': '/bc/ticker' },
		}

	def ticker(self, quote_currency, base_currency):
		ticker_data = self.ticker_data(quote_currency, base_currency)['ticker']

		ticker = {
			'price_units': base_currency,
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
		self.base_url = 'https://api.bitfinex.com/v1'
		self.tickers = {
			('btc', 'usd'): { 'url': '/ticker/btcusd' },
			('ltc', 'usd'): { 'url': '/ticker/ltcusd' },
			('ltc', 'btc'): { 'url': '/ticker/ltcbtc' },
		}

	def ticker(self, quote_currency, base_currency):
		ticker_data = self.ticker_data(quote_currency, base_currency)

		ticker = {
			'price_units': base_currency,
			'bid': self.float_price(ticker_data['bid']),
			'ask': self.float_price(ticker_data['ask']),
			'last': self.float_price(ticker_data['last_price']),
			'timestamp': int(float(ticker_data['timestamp'])),
		}

		return ticker

