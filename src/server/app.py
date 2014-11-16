#! /usr/bin/env python

import tornado.ioloop
import tornado.web
import routes as rt
import projector as ws

# APPLICATION GLOBALS
global ProjSocket

# APPLICATION ROUTING
application = tornado.web.Application([
    (r"/", rt.MainHandler),
    (r'/stack', rt.StackHandler),
    (r'/push', rt.PushToScreen),
    (r'/socket', ws.ProjectorWebSocket),
    (r"/render/(.*)", tornado.web.StaticFileHandler, {"path": "../render"}),
])

if __name__ == "__main__":
    application.listen(8888)
    print("Listening on port 8888")
    tornado.ioloop.IOLoop.instance().start()
