import tornado.web
import tornado.websocket
import json

json_data = open('cards.json').read()
stack = json.loads(json_data)

global ProjSocket
ProjSocket = None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class StackHandler(tornado.web.RequestHandler):
	def get(self):
		self.write(json.dumps(stack))

class PushToScreen(tornado.web.RequestHandler):
	def post(self):
		print self.request.body
		if ProjSocket:
			self.request.body['type'] = 'push'
			ProjSocket.write_message(json.dumps(self.request.body))
			self.write("SUCCESS")
		else:
			self.write("NO SOCKET")

class UpdateVar(tornado.web.RequestHandler):
	def get(self):
		if ProjSocket:
			self.request.arguments['type'] = 'cvar'
			ProjSocket.write_message(json.dumps(self.request.arguments))
			self.write("SUCCESS")
		else:
			self.write("NO SOCKET")


# Communicates with the projector HTML5 screen
class ProjectorWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
    	global ProjSocket
    	ProjSocket = self
        print "Opened socket to Projector"

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print "WebSocket closed"