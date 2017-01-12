from flask import redirect, url_for, request
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import UserMixin, RoleMixin, login_required, current_user

from database import db


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    """Allows for distinguishing castes of users. Currently access control
    is only based on whether a person is a registered user (see accessible)
    but this would let you get fancy in the future."""

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    """Registered users of the sight, copied from the setup found in the
    flask admin auth example here:

    https://github.com/flask-admin/flask-admin/blob/master/examples/auth/app.py
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, primary_key=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    

def accessible() -> bool:
    """Simple authentication that validates the current user. If they have
    not logged in current_user.is_authenticated returns False."""

    if current_user.is_authenticated:
        return True
    return False


class BeehiveAdminIndexView(AdminIndexView):
    """Custom index view that is responsible for hiding the root admin page."""

    @expose()
    def index(self):
        if not accessible():
            return redirect(url_for('security.login', next=request.url))    
        return self.render(self._template)


class BeehiveModelView(ModelView):
    """Custom model views that hide pages for individual database models."""
        
    def _handle_view(self, name, **kwargs):
        if not accessible():
            return redirect(url_for('security.login', next=request.url))    
