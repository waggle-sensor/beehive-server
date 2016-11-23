from . import web

@web.route('/')
def root():
    return 'found web ROOT'
    
@web.route('/search/')
def search():
    return 'found web Search'
