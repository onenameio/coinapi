DEBUG = True

CURRENCY_PAIRS = [
	{ 'name': 'Bitcoin / US Dollars', 'symbols': ('btc','usd') },
	{ 'name': 'Bitcoin / Euros', 'symbols': ('btc','eur') },
	{ 'name': 'Bitcoin / Chinese Yuan', 'symbols': ('btc','cny') },
	{ 'name': 'Bitcoin / Japanese Yen', 'symbols': ('btc','jpy') },
	{ 'name': 'Bitcoin / Canadian Dollars', 'symbols': ('btc','cad') },
	{ 'name': 'Litecoin / US Dollars', 'symbols': ('ltc','usd') },
	{ 'name': 'Litecoin / Euros', 'symbols': ('ltc','eur') },
	{ 'name': 'Litecoin / Bitcoin', 'symbols': ('ltc','btc') },
	{ 'name': 'Namecoin / US Dollars', 'symbols': ('nmc','usd') },
	{ 'name': 'Namecoin / Euros', 'symbols': ('nmc','eur') },
	{ 'name': 'Namecoin / Bitcoin', 'symbols': ('nmc','btc') },
	{ 'name': 'Peercoin / Bitcoin', 'symbols': ('ppc','btc') },
	{ 'name': 'Primecoin / Bitcoin', 'symbols': ('xpm','btc') },
	{ 'name': 'Novacoin / Bitcoin', 'symbols': ('nvc','btc') },
	{ 'name': 'Terracoin / Bitcoin', 'symbols': ('trc','btc') },
]

RESOURCES = { "groups": [
	{
		"name": "Must Visits",
		"items": [
			{
			"name": "Bitcoin.org",
			"url": "http://bitcoin.org/",
			"description": "The Official Website of the Bitcoin Project."
			},
			{
			"name": "Bitcoin Foundation",
			"url": "https://bitcoinfoundation.org/",
			"description": "Bitcoin Foundation standardizes, protects and promotes the use of Bitcoin cryptographic money for the benefit of users worldwide."
			},
			{
			"name": "Bitcoin Wiki",
			"url": "https://en.bitcoin.it/wiki/Main_Page",
			"description": ""
			},
			{
			"name": "We Use Coins",
			"url": "https://www.weusecoins.com/en/",
			"description": ""
			},
			{
			"name": "Bitcoin Mining",
			"url": "http://www.bitcoinmining.com/",
			"description": ""
			},
		],
	},
		{
		"name": "News",
		"items": [
			{
			"name": "CoinDesk",
			"url": "http://www.coindesk.com/",
			"description": "Covers news and analysis on the trends, price movements, technologies, companies and people in the bitcoin and digital currency world."
			},
			{
			"name": "The Genesis Block",
			"url": "http://thegenesisblock.com/",
			"description": ""
			},
			{
			"name": "Bitcoin Magazine",
			"url": "http://bitcoinmagazine.com/",
			"description": ""
			},
			{
			"name": "Bitcoin Forum",
			"url": "https://bitcointalk.org/index.php?board=77.0",
			"description": ""
			},
			{
			"name": "The Daily Bitcoin",
			"url": "http://thedailybitcoin.com/",
			"description": ""
			},
			{
			"name": "CryptoJunky",
			"url": "http://cryptojunky.com/blog/",
			"description": ""
			},
			
		],
	},
	{
		"name": "Block Exploration",
		"items": [
			{
			"name": "Blockchain.info",
			"url": "https://blockchain.info/",
			"description": "System to navigate the bitcoin block chain."
			},
			{
			"name": "Bitcoin Block Explorer",
			"url": "http://blockexplorer.com/",
			"description": ""
			},
			{
			"name": "",
			"url": "",
			"description": ""
			},
		],
	},
	{
		"name": "Culture",
		"items": [
			{
			"name": "BitcoinFilm.org",
			"url": "http://bitcoinfilm.org/",
			"description": ""
			},
			{
			"name": "",
			"url": "",
			"description": ""
			},
		],
	},
	{
		"name": "Learning",
		"items": [
			{
			"name": "How Bitcoin Works Under the Hood",
			"url": "https://www.youtube.com/watch?v=Lx9zgZCMqXE",
			"description": ""
			},
			{
			"name": "Khan Academy",
			"url": "https://www.khanacademy.org/economics-finance-domain/core-finance/money-and-banking/bitcoin/v/bitcoin-what-is-it",
			"description": ""
			},
			{
			"name": "Let's Talk Bitcoin",
			"url": "http://letstalkbitcoin.com/",
			"description": ""
			},	
		],
	},
	{
		"name": "Charts",
		"items": [
			{
			"name": "Bitcoin Wisdom",
			"url": "http://bitcoinwisdom.com/",
			"description": "Live Bitcoin/Litecoin charts."
			},
			{
			"name": "Coin Market Cap",
			"url": "http://coinmarketcap.com/",
			"description": "Crypto-Currency Market Capitalizations"
			},
			{
			"name": "BitcoinX",
			"url": "http://www.bitcoinx.com/",
			"description": "A variety of tools and charts, including financial and technical data, related to the bitcoin network and markets."
			},
			{
			"name": "Bitcoin Charts",
			"url": "http://bitcoincharts.com/charts/",
			"description": ""
			},
			{
			"name": "ZeroBlock",
			"url": "http://www.zeroblock.com/",
			"description": ""
			},
			{
			"name": "ZeroBlock",
			"url": "http://www.zeroblock.com/",
			"description": ""
			},
			{
			"name": "RTBTC",
			"url": "http://bitcoin.clarkmoody.com/",
			"description": ""
			},
		],
	},
	{
		"name": "Wallets",
		"items": [
			{
			"name": "Bitcoin.org: Choose Your Wallet",
			"url": "http://bitcoin.org/en/choose-your-wallet",
			"description": "Directory of Bitcoin Wallets"
			},
			{
			"name": "Bitcoin-Qt",
			"url": "http://bitcoin.org/en/download",
			"description": "The original Bitcoin client."
			},
			{
			"name": "MultiBit",
			"url": "https://multibit.org/",
			"description": "A lightweight Bitcoin client."
			},
		],
	},
	{
		"name": "Coin Merchants",
		"items": [
			{
			"name": "useBitcoins.info",
			"url": "http://usebitcoins.info/",
			"description": ""
			},
			{
			"name": "Coinmap.org",
			"url": "http://coinmap.org/",
			"description": ""
			},
			{
			"name": "",
			"url": "",
			"description": ""
			},
		],
	},
	{
		"name": "Merchant Tools",
		"items": [
			{
			"name": "Shopping Cart Interfaces",
			"url": "https://en.bitcoin.it/wiki/Category:Shopping_Cart_Interfaces",
			"description": "Software for providing online shopping websites a method for handling payment in bitcoins."
			},
			{
			"name": "Bitcoin100",
			"url": "http://bitcoin100.org/",
			"description": "Bitcoin100 donates the Bitcoin equivalent of $1000 to charities that prominently display an option for supporters to contribute via Bitcoin on their website."
			},
		],
	},
	{
		"name": "Data",
		"items": [
			{
			"name": "Quandl Bitcoin Datasets",
			"url": "http://www.quandl.com/search/bitcoin",
			"description": "Listing of various Bitcoin datasets."
			},
			{
			"name": "CoinDesk Bitcoin Price Index",
			"url": "http://www.coindesk.com/price/",
			"description": "An average of bitcoin prices across leading global exchanges that meet criteria specified by the BPI."
			},
		],
	},
]
}
