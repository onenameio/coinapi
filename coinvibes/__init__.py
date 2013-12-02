from flask import Flask

app = Flask(__name__)
app.config.from_object('coinvibes.settings')

import coinvibes.views
import coinvibes.exchange_apis
import coinvibes.utils
import coinvibes.api_v1
