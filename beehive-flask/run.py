from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

from beehive_blueprints.admin import admin
from beehive_blueprints.api import api
from beehive_blueprints.web import web


SQLALCHEMY_DATABASE_URI = "mysql://waggle:waggle@172.18.0.4/waggle"


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

# app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(web, url_prefix="")

db = SQLAlchemy(app)
base = automap_base()
base.prepare(db.engine, reflect=True)

admin = Admin(app, name='beehive-server', template_mode='bootstrap3')
for table in base.classes:
    admin.add_view(ModelView(table, db.session))


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=True)

