#!/usr/bin/env python
import web

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'world'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", 9999))
    app.run()

