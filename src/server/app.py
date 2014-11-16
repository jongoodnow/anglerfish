#! /usr/bin/env python

import tornado.ioloop
import tornado.web
import routes as rt

# APPLICATION GLOBALS
global ProjSocket

# APPLICATION ROUTING
application = tornado.web.Application([
    (r"/", rt.MainHandler),
    (r'/stack', rt.StackHandler),
    (r'/push', rt.PushToScreen),
    (r'/update', rt.UpdateVar),
    (r'/socket', rt.ProjectorWebSocket),
    (r'/add', rt.AddCard),
    (r"/render/(.*)", tornado.web.StaticFileHandler, {"path": "../render"}),
    (r"/control/(.*)", tornado.web.StaticFileHandler, {"path": "../control-app"}),
    (r"/contribute/(.*)", tornado.web.StaticFileHandler, {"path": "../add-app"}),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "./static"}),
])

if __name__ == "__main__":
    application.listen(8888)
    print("Listening on port 8888")
    tornado.ioloop.IOLoop.instance().start()
