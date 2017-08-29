from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from beehive_blueprints.api import api
from beehive_blueprints.web import web

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://waggle:waggle@beehive-mysql/waggle'
app.register_blueprint(web, url_prefix='')
app.register_blueprint(api, url_prefix='/api')

db = SQLAlchemy()
db.init_app(app)
db.reflect(app=app)


@web.route('/v2/')
def v2_index():
    return 'starting a-new'


@web.route('/v2/nodes')
def v2_nodes():
    return 'starting a-new'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
