from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from beehive_blueprints.api import api
from beehive_blueprints.web import web

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://waggle:waggle@beehive-mysql/waggle'
app.register_blueprint(web, url_prefix='')
app.register_blueprint(api, url_prefix='/api')

db = SQLAlchemy(app)
db.reflect()


@app.route('/v2/')
def v2_index():
    return 'starting a-new'


@app.route('/v2/nodes')
def v2_nodes():
    nodes = []

    for node_id, name in db.engine.execute('SELECT node_id, name FROM nodes'):
        nodes.append((node_id, name))

    return str(nodes)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
