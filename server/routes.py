import tornado.web
import server.arduino as ard

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")