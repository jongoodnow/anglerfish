#! /usr/bin/env python

import tornado.ioloop
import tornado.web
import server.routes as rt

application = tornado.web.Application([
    (r"/", rt.MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    print("Listening on port 8888")
    tornado.ioloop.IOLoop.instance().start()