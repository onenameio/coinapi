import json
import requests
import traceback
from flask import abort
from coinvibes.utils import APIError, remove_non_ascii, remove_non_numeric

CURRENCY_NAMES = {
	'btc': { 'proper': 'Bitcoin', 'singular': 'bitcoin', 'plural': 'bitcoins' },
	'ltc': { 'proper': 'Litecoin', 'singular': 'litecoin', 'plural': 'litecoins' },
	'nmc': { 'proper': 'Namecoin', 'singular': 'namecoin', 'plural': 'namecoins' },
	'ppc': { 'proper': 'Peercoin', 'singular': 'namecoin', 'plural': 'namecoins' },
	'xpm': { 'proper': 'Primecoin', 'singular': 'primecoin', 'plural': 'primecoins' },
	'nvc': { 'proper': 'Novacoin', 'singular': 'novacoin', 'plural': 'novacoins' },
	'trc': { 'proper': 'Terracoin', 'singular': 'terracoin', 'plural': 'terracoins' },
	'qrk': { 'proper': 'QuarkCoin', 'singular': 'quarkcoin', 'plural': 'quarkcoins' },
	'mec': { 'proper': 'Megacoin', 'singular': 'megacoin', 'plural': 'megacoins' },
	'wdc': { 'proper': 'WorldCoin', 'singular': 'worldcoin', 'plural': 'worldcoins' },
	'pts': { 'proper': 'ProtoShares', 'singular': 'protoshare', 'plural': 'protoshares' },
	'ftc': { 'proper': 'Feathercoin', 'singular': 'feathercoin', 'plural': 'feathercoins' },
	'frc': { 'proper': 'Freicoin', 'singular': 'freicoin', 'plural': 'freicoins' },
	'anc': { 'proper': 'Anoncoin', 'singular': 'anoncoin', 'plural': 'anoncoins' },

	'usd': { 'proper': 'US dollar', 'plural': 'US dollars' },
	'eur': { 'proper': 'euro', 'plural': 'euros' },
	'cny': { 'proper': 'Chinese yuan', 'plural': 'Chinese yuan' },
	'jpy': { 'proper': 'Japanese yen', 'plural': 'Japanese yen' },
	'cad': { 'proper': 'Canadian dollar', 'plural': 'Canadian dollars' },
	'aud': { 'proper': 'Australian dollar', 'plural': 'Australian dollars' },
	'chf': { 'proper': 'Swiss francs', 'plural': 'Swiss francs' },
	'dkk': { 'proper': 'Danish krone', 'plural': 'Danish kroner' },
	'gbp': { 'proper': 'British pound', 'plural': 'British pounds' },
	'hkd': { 'proper': 'Hong Kong dollar', 'plural': 'Hong Kong dollars' },
	'nok': { 'proper': 'Norwegian kroner', 'plural': 'Norwegian kroner' },
	'nzd': { 'proper': 'New Zealand dollar', 'plural': 'New Zealand dollars' },
	'pln': { 'proper': 'Polish zloty', 'plural': 'Polish zlotys' },
	'rub': { 'proper': 'Russian ruble', 'plural': 'Russian rubles' },
	'sek': { 'proper': 'Swedish krone', 'plural': 'Swedish kroner' },
	'sgd': { 'proper': 'Singapore dollar', 'plural': 'Singapore dollars' },
	'thb': { 'proper': 'Thai baht', 'plural': 'Thai bahts' },
}

def format_currency(currency_code):
	return {
		'code': currency_code,
		'name': CURRENCY_NAMES[currency_code]['proper'],
	}

def format_currency_pair(quote_currency, base_currency):
	return {
		'quote_currency': {
			'code': quote_currency,
			'name': CURRENCY_NAMES[quote_currency]['proper'],
		},
		'base_currency': {
			'code': base_currency,
			'name': CURRENCY_NAMES[base_currency]['proper'],
		},
	}

class MasterExchangeAPI():
	def __init__(self, exchange_apis):
		self.api_root_url = '/api/v1'
		self.exchange_apis = exchange_apis
		self.currency_names = CURRENCY_NAMES

	def get_exchange_api(self, exchange_slug):
		for exchange_api in self.exchange_apis:
			if exchange_slug == exchange_api.slug:
				return exchange_api
		return None

	def get_exchange_data(self, exchange_slug):
		exchange_api = self.get_exchange_api(exchange_slug)

		exchange_data = {
			'name': exchange_api.name,
			'slug': exchange_api.slug,
			'url': self.api_root_url + '/tickers/' + exchange_api.slug,
			'tickers': [],
		}
		
		for currency_pair in exchange_api.currency_pairs:
			quote_currency = currency_pair[0]
			base_currency = currency_pair[1]

			currency_pair_data = format_currency_pair(
				quote_currency, base_currency)
			currency_pair_data['url'] = self.api_root_url + '/tickers/' + \
				exchange_api.slug + '/' + quote_currency + '_' + base_currency
			exchange_data['tickers'].append(currency_pair_data)
		
		return exchange_data

	def get_currency_pairs(self, quote_currency=None, base_currency=None):
		currency_pair_dict = {}
		for exchange_api in self.exchange_apis:
			for currency_pair in exchange_api.currency_pairs:
				if quote_currency:
					if currency_pair[0] != quote_currency:
						continue
				if base_currency:
					if currency_pair[1] != base_currency:
						continue
				currency_pair_dict[currency_pair] = True

		currency_pairs = []

		for currency_pair in currency_pair_dict:
			currency_pair_data = format_currency_pair(currency_pair[0],
													  currency_pair[1])
			currency_pairs.append(currency_pair_data)

		return currency_pairs

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

	def raw_ticker(self, quote_currency, base_currency):
		currency_pair = self.currency_pairs.get((quote_currency, base_currency))
		if currency_pair:
			try:
				r = requests.get(self.base_url + currency_pair['ticker_url'],
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

	def get_description(self):
		return {
			'name': self.name,
			'slug': self.slug
		}

class MtGoxAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'Mt. Gox'
		self.slug = 'mtgox'
		self.base_url = 'http://data.mtgox.com/api/2'
		self.currency_pairs = {
			('btc', 'usd'): { 'ticker_url': '/BTCUSD/money/ticker' },
			('btc', 'jpy'): { 'ticker_url': '/BTCJPY/money/ticker' },
			('btc', 'eur'): { 'ticker_url': '/BTCEUR/money/ticker' },
			('btc', 'cny'): { 'ticker_url': '/BTCCNY/money/ticker' },
			('btc', 'cad'): { 'ticker_url': '/BTCCAD/money/ticker' },
			('btc', 'aud'): { 'ticker_url': '/BTCAUD/money/ticker' },
			('btc', 'chf'): { 'ticker_url': '/BTCCHF/money/ticker' },
			('btc', 'dkk'): { 'ticker_url': '/BTCDKK/money/ticker' },
			('btc', 'gbp'): { 'ticker_url': '/BTCGBP/money/ticker' },
			('btc', 'hkd'): { 'ticker_url': '/BTCHKD/money/ticker' },
			('btc', 'nok'): { 'ticker_url': '/BTCNOK/money/ticker' },
			('btc', 'nzd'): { 'ticker_url': '/BTCNZD/money/ticker' },
			('btc', 'pln'): { 'ticker_url': '/BTCPLN/money/ticker' },
			('btc', 'rub'): { 'ticker_url': '/BTCRUB/money/ticker' },
			('btc', 'sek'): { 'ticker_url': '/BTCSEK/money/ticker' },
			('btc', 'sgd'): { 'ticker_url': '/BTCSGD/money/ticker' },
			('btc', 'thb'): { 'ticker_url': '/BTCTHB/money/ticker' },
			#('ltc', 'usd'): { 'ticker_url': '/LTCUSD/money/ticker' },
			#('ltc', 'cny'): { 'ticker_url': '/LTCCNY/money/ticker' },
			#('ltc', 'jpy'): { 'ticker_url': '/LTCJPY/money/ticker' },
			#('ltc', 'eur'): { 'ticker_url': '/LTCEUR/money/ticker' },
			#('ltc', 'cad'): { 'ticker_url': '/LTCCAD/money/ticker' },
			#('nmc', 'usd'): { 'ticker_url': '/NMCUSD/money/ticker' },
		}

	def ticker(self, quote_currency, base_currency):
		raw_ticker = self.raw_ticker(quote_currency, base_currency)['data']

		return {
			'quote_currency': format_currency(quote_currency),
			'base_currency': format_currency(base_currency),
			'vol': float(raw_ticker['vol']['value_int']),
			'bid': self.float_price(raw_ticker['buy']['display']),
			'ask': self.float_price(raw_ticker['sell']['display']),
			'high': self.float_price(raw_ticker['high']['display']),
			'low': self.float_price(raw_ticker['low']['display']),
			'exchange_timestamp': int(raw_ticker['now'])/(1000*1000),
			'last': self.float_price(raw_ticker['last']['display']),
			'average': self.float_price(raw_ticker['avg']['display']),
			'vwap': self.float_price(raw_ticker['vwap']['display']),
		}

class BTCeAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'BTC-e'
		self.slug = 'btce'
		self.base_url = 'https://btc-e.com/api/2'
		self.currency_pairs = {
			('btc', 'usd'): { 'ticker_url': '/btc_usd/ticker' },
			('btc', 'eur'): { 'ticker_url': '/btc_eur/ticker' },
			('btc', 'rub'): { 'ticker_url': '/btc_rur/ticker' },
			('ltc', 'usd'): { 'ticker_url': '/ltc_usd/ticker' },
			('ltc', 'eur'): { 'ticker_url': '/ltc_eur/ticker' },
			('ltc', 'btc'): { 'ticker_url': '/ltc_btc/ticker' },
			('ltc', 'rub'): { 'ticker_url': '/ltc_rur/ticker' },
			('nmc', 'btc'): { 'ticker_url': '/nmc_btc/ticker' },
			('nmc', 'usd'): { 'ticker_url': '/nmc_usd/ticker' },
			('ppc', 'btc'): { 'ticker_url': '/ppc_btc/ticker' },
			('ppc', 'usd'): { 'ticker_url': '/ppc_usd/ticker' },
			('xpm', 'btc'): { 'ticker_url': '/xpm_btc/ticker' },
			('nvc', 'btc'): { 'ticker_url': '/nvc_btc/ticker' },
			('nvc', 'usd'): { 'ticker_url': '/nvc_usd/ticker' },
			('trc', 'btc'): { 'ticker_url': '/trc_btc/ticker' },
			('ftc', 'btc'): { 'ticker_url': '/ftc_btc/ticker' },
			('usd', 'rub'): { 'ticker_url': '/usd_rur/ticker' },
			('eur', 'usd'): { 'ticker_url': '/eur_usd/ticker' },
		}

	def ticker(self, quote_currency, base_currency):
		raw_ticker = self.raw_ticker(quote_currency, base_currency)['ticker']

		return {
			'quote_currency': format_currency(quote_currency),
			'base_currency': format_currency(base_currency),
			'vol': float(raw_ticker['vol']),
			'bid': raw_ticker['buy'],
			'ask': raw_ticker['sell'],
			'high': raw_ticker['high'],
			'low': raw_ticker['low'],
			'exchange_timestamp': int(raw_ticker['server_time']),
			'last': raw_ticker['last'],
			'average': raw_ticker['avg'],
		}

class BitstampAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'Bitstamp'
		self.slug = 'bitstamp'
		self.base_url = 'https://www.bitstamp.net/api'
		self.currency_pairs = {
			('btc', 'usd'): { 'ticker_url': '/ticker/' }
		}

	def ticker(self, quote_currency, base_currency):
		raw_ticker = self.raw_ticker(quote_currency, base_currency)

		return {
			'quote_currency': format_currency(quote_currency),
			'base_currency': format_currency(base_currency),
			'volume': float(raw_ticker['volume']),
			'bid': self.float_price(raw_ticker['bid']),
			'ask': self.float_price(raw_ticker['ask']),
			'high': self.float_price(raw_ticker['high']),
			'low': self.float_price(raw_ticker['low']),
			'exchange_timestamp': int(raw_ticker['timestamp']),
		}

class KrakenAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'Kraken'
		self.slug = 'kraken'
		self.base_url = 'https://api.kraken.com/0/public'
		self.currency_pairs = {
			('btc', 'usd'): { 'ticker_url': '/Ticker?pair=XXBTZUSD' },
			('btc', 'eur'): { 'ticker_url': '/Ticker?pair=XXBTZEUR' },
			('nmc', 'usd'): { 'ticker_url': '/Ticker?pair=XNMCZUSD' },
			('nmc', 'eur'): { 'ticker_url': '/Ticker?pair=XNMCZEUR' },
			('ltc', 'usd'): { 'ticker_url': '/Ticker?pair=XLTCZUSD' },
			('ltc', 'eur'): { 'ticker_url': '/Ticker?pair=XLTCZEUR' },
			('btc', 'nmc'): { 'ticker_url': '/Ticker?pair=XXBTXNMC' },
		}

	def ticker(self, quote_currency, base_currency):
		raw_ticker = self.raw_ticker(quote_currency, base_currency)

		currency_pair = self.currency_pairs.get((quote_currency, base_currency))
		pair_name = currency_pair.get('ticker_url').strip('/Ticker?pair=')
		raw_ticker = raw_ticker['result'][pair_name]

		return {
			'quote_currency': format_currency(quote_currency),
			'base_currency': format_currency(base_currency),
			'volume': self.float_price(raw_ticker['v'][0]),
			'bid': self.float_price(raw_ticker['b'][0]),
			'ask': self.float_price(raw_ticker['a'][0]),
			'high': self.float_price(raw_ticker['h'][0]),
			'low': self.float_price(raw_ticker['l'][0]),			
			'average': self.float_price(raw_ticker['p'][0]),
		}

class BTCChinaAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'BTC China'
		self.slug = 'btcchina'
		self.base_url = 'https://vip.btcchina.com'
		self.currency_pairs = {
			('btc', 'cny'): { 'ticker_url': '/bc/ticker' },
		}

	def ticker(self, quote_currency, base_currency):
		raw_ticker = self.raw_ticker(quote_currency, base_currency)['ticker']

		return {
			'quote_currency': format_currency(quote_currency),
			'base_currency': format_currency(base_currency),
			'vol': float(raw_ticker['vol']),
			'bid': self.float_price(raw_ticker['buy']),
			'ask': self.float_price(raw_ticker['sell']),
			'high': self.float_price(raw_ticker['high']),
			'low': self.float_price(raw_ticker['low']),
			'last': self.float_price(raw_ticker['last']),
		}

class BitfinexAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'Bitfinex'
		self.slug = 'bitfinex'
		self.base_url = 'https://api.bitfinex.com/v1'
		self.currency_pairs = {
			('btc', 'usd'): { 'ticker_url': '/ticker/btcusd' },
			('ltc', 'usd'): { 'ticker_url': '/ticker/ltcusd' },
			('ltc', 'btc'): { 'ticker_url': '/ticker/ltcbtc' },
		}

	def ticker(self, quote_currency, base_currency):
		raw_ticker = self.raw_ticker(quote_currency, base_currency)

		return {
			'quote_currency': format_currency(quote_currency),
			'base_currency': format_currency(base_currency),
			'bid': self.float_price(raw_ticker['bid']),
			'ask': self.float_price(raw_ticker['ask']),
			'last': self.float_price(raw_ticker['last_price']),
			'exchange_timestamp': int(float(raw_ticker['timestamp'])),
		}

class CoinbaseAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'Coinbase'
		self.slug = 'coinbase'
		self.base_url = 'https://coinbase.com/api/v1'
		self.currency_pairs = {
			('btc', 'usd'): { 'buy_ticker_url': '/prices/buy', 'sell_ticker_url': '/prices/sell' },
		}

	def raw_ticker(self, quote_currency, base_currency):
		currency_pair = self.currency_pairs.get((quote_currency, base_currency))
		if currency_pair:
			try:
				r1 = requests.get(self.base_url + currency_pair['buy_ticker_url'],
								 timeout=4, verify=False)
				r2 = requests.get(self.base_url + currency_pair['sell_ticker_url'],
								 timeout=4, verify=False)
			except requests.exceptions.Timeout:
				raise APIError('Timeout')
		else:
			abort(404)

		try:
			data1 = json.loads(r1.text)
			data2 = json.loads(r2.text)
		except ValueError:
			traceback.print_exc()
			data = None

		data = { "buy": data1, "sell": data2 }

		return data

	def ticker(self, quote_currency, base_currency):
		raw_ticker = self.raw_ticker(quote_currency, base_currency)

		return {
			'bid': self.float_price(raw_ticker['buy']['amount']),
			'ask': self.float_price(raw_ticker['sell']['amount']),
			'quote_currency': format_currency(quote_currency),
			'base_currency': format_currency(base_currency),
		}

class BterAPI(ExchangeAPI):
	def __init__(self):
		self.name = 'Bter'
		self.slug = 'bter'
		self.base_url = 'https://bter.com/api/1'
		self.currency_pairs = {
			('btc', 'cny'): { 'ticker_url': '/ticker/btc_cny' },
			('ltc', 'cny'): { 'ticker_url': '/ticker/ltc_cny' },
			('nmc', 'cny'): { 'ticker_url': '/ticker/nmc_cny' },
			('ppc', 'cny'): { 'ticker_url': '/ticker/ppc_cny' },
			#('trc', 'cny'): { 'url': '/ticker/trc_cny' },
			('xpm', 'cny'): { 'ticker_url': '/ticker/xpm_cny' },
			('ftc', 'cny'): { 'ticker_url': '/ticker/ftc_cny' },
			#('frc', 'cny'): { 'url': '/ticker/frc_cny' },
			('pts', 'cny'): { 'ticker_url': '/ticker/pts_cny' },
			#('qrk', 'cny'): { 'url': '/ticker/qrk_cny' },
			#('nvc', 'cny'): { 'url': '/ticker/nvc_cny' },
			#('mec', 'cny'): { 'url': '/ticker/mec_cny' },
			#('wdc', 'cny'): { 'url': '/ticker/wdc_cny' },

			#('ftc', 'ltc'): { 'url': '/ticker/ftc_ltc' },
			#('frc', 'ltc'): { 'url': '/ticker/frc_ltc' },
			#('ppc', 'ltc'): { 'url': '/ticker/ppc_ltc' },
			#('nmc', 'ltc'): { 'url': '/ticker/nmc_ltc' },
			#('trc', 'ltc'): { 'url': '/ticker/trc_ltc' },
			#('wdc', 'ltc'): { 'url': '/ticker/wdc_ltc' },

			('ltc', 'btc'): { 'ticker_url': '/ticker/ltc_btc' },
			('nmc', 'btc'): { 'ticker_url': '/ticker/nmc_btc' },
			('ppc', 'btc'): { 'ticker_url': '/ticker/ppc_btc' },
			#('trc', 'btc'): { 'url': '/ticker/trc_btc' },
			('xpm', 'btc'): { 'ticker_url': '/ticker/xpm_btc' },

			('ftc', 'btc'): { 'ticker_url': '/ticker/ftc_btc' },
			#('frc', 'btc'): { 'url': '/ticker/frc_btc' },
			('pts', 'btc'): { 'ticker_url': '/ticker/pts_btc' },
			#('qrk', 'btc'): { 'url': '/ticker/qrk_btc' },
			#('nvc', 'btc'): { 'url': '/ticker/nvc_btc' },
			#('mec', 'btc'): { 'url': '/ticker/mec_btc' },
			#('wdc', 'btc'): { 'url': '/ticker/wdc_btc' },
		}

	def ticker(self, quote_currency, base_currency):
		raw_ticker = self.raw_ticker(quote_currency, base_currency)

		return {
			'quote_currency': format_currency(quote_currency),
			'base_currency': format_currency(base_currency),
			'bid': raw_ticker['buy'],
			'ask': raw_ticker['sell'],
			'last': raw_ticker['last'],
			'high': raw_ticker['high'],
			'low': raw_ticker['low'],
			'average': raw_ticker['avg'],
		}

master_exchange_api = MasterExchangeAPI([
	BitstampAPI(), MtGoxAPI(), BTCeAPI(), KrakenAPI(), BTCChinaAPI(),
	BitfinexAPI(), CoinbaseAPI(), BterAPI()
])
