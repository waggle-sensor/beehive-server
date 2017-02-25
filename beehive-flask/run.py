from flask import Blueprint, render_template
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import UserMixin, RoleMixin, login_required

from flask import Flask, url_for
from flask_admin import Admin, helpers
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

from beehive_blueprints.admin import admin
from beehive_blueprints.api import api
from beehive_blueprints.web import web
from database import db
from models import BeehiveAdminIndexView, BeehiveModelView, Role, User


#SQLALCHEMY_DATABASE_URI = "mysql://waggle:waggle@172.18.0.4/waggle"
#SQLALCHEMY_DATABASE_URI = "mysql://waggle:waggle@172.18.0.6/waggle"
SQLALCHEMY_DATABASE_URI = "mysql://waggle:waggle@beehive-mysql/waggle"

app = Flask(__name__)

# Simple application configuration, these ought to be environment vars

# Change this on production, it gives everyone access to the flask debugger
# on an uncaught exception (which literally gives them a shell inside your app)
#app.config["DEBUG"] = True  

# Also change this
app.config["SECRET_KEY"] = "highly secret"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(web, url_prefix="")

# Creates a sqlalchemy engine with the URI found in the app's config
# This lets you manage database sessions, execute sql, and lots more
db.init_app(app)
# Sets up login management and access control 
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
# Sets up the sqlalchemy based admin page
admin = Admin(
    app=app, 
    index_view=BeehiveAdminIndexView(),
    name='beehive-server', 
    template_mode='bootstrap3'
)


def create_default_user():

    db.metadata.create_all(bind = db.engine)
    existing_user = db.session.query(User).first()
    if existing_user:
        return
    
    default_user = User(email="admin@waggle.net", password="changeme", id = 0, active = True)
    db.session.add(default_user)
    db.session.commit()
    


if __name__ == "__main__":

    # Reflects the existing mysql schema and registers each table with admin
    # NOTE: For a table to be eligible for registration with the admin panel
    # NOTE: it needs to have an auto incremented primary key
    with app.app_context():
        create_default_user()

        base = automap_base()
        base.prepare(db.engine, reflect=True)
        for table in base.classes:
            admin.add_view(BeehiveModelView(table, db.session))

    # Vamonos!
    app.run(host = '0.0.0.0')


