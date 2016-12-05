from . import web 

@web.route('/')
def web_root():
    return 'You found web!!!'

@web.route('/search/')
def web_search():
    return 'found web Search'
