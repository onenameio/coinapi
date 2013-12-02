from flask import Flask

app = Flask(__name__)
app.config.from_object('api.settings')

import api.views
import api.exchange_apis
import api.utils