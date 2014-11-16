import tornado.web
import json

json_data = open('cards.json').read()
stack = json.loads(json_data)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class StackHandler(tornado.web.RequestHandler):
	def get(self):
		self.write(json.dumps(stack))

class PushToScreen(tornado.web.RequestHandler):
	def get(self):
		if ProjSocket:
			print self.get_query_arguments()
			global ProjSocket.write_message(JSON.dumps(self.get_query_arguments()))
			self.write("SUCCESS")
		else:
			self.write("NO SOCKET")