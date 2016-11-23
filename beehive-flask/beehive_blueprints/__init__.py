from flask import Flask

from .admin import admin
from .api   import api
from .web   import web

app = Flask(__name__)

# Puts the API blueprint on api.U2FtIEJsYWNr.com.
app.register_blueprint(admin, url_prefix = '/admin')
app.register_blueprint(api,   url_prefix = '/api')
app.register_blueprint(web,   url_prefix = '')
