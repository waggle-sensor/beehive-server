from . import admin

@admin.route('/')
def admin_root():
    return 'You found admin!!!'
