from flask import Flask

app = Flask(__name__)
app.config.from_object('coinvibes.settings')

import coinvibes.views
import coinvibes.exchange_apis
import coinvibes.utils
import coinvibes.api_v1

import analytics

analytics.init('5asae1e0a2gpb8uu0sx0')

## use HerokuRequest class so we get real IPs
app.request_class = utils.ProxiedRequest