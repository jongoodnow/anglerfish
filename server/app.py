import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid

from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

import routes

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

# Making this a non-singleton is left as an exercise for the reader.
global_message_buffer = routes.MessageBuffer()

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", routes.MainHandler),
            (r"/auth/login", routes.AuthLoginHandler),
            (r"/auth/logout", routes.AuthLogoutHandler),
            (r"/a/message/new", routes.MessageNewHandler),
            (r"/a/message/updates", routes.MessageUpdatesHandler),
            ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        login_url="/auth/login",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
        )
    app.listen(options.port)
    print("Listening on Port 8888")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()