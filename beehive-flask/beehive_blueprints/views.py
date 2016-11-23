from . import app

@app.route('/search', subdomain='api')
def api_search():
    return 'api_search() found...'
