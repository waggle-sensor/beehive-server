from . import admin

@admin.route('/')
def admin_root():
    return 'You found admin!!!'

@admin.route('/search/')
def search():
    return 'found admin Search'
