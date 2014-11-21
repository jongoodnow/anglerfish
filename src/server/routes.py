import tornado.web
import tornado.websocket
import urlparse
import json
import uuid
import StringIO
import random
import string
import os
from PIL import Image

json_data = open(os.path.join(os.path.dirname(__file__), 'cards.json')).read()
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
		if ProjSocket:
			body = json.loads(urlparse.unquote(self.request.body))
			body['type'] = 'push'
			ProjSocket.write_message(json.dumps(body))
			self.write("SUCCESS")
		else:
			self.write("NO SOCKET")

class UpdateVar(tornado.web.RequestHandler):
	def get(self):
		print self.request.arguments
		if ProjSocket:
			self.request.arguments['type'] = 'cvar'
			ProjSocket.write_message(json.dumps(self.request.arguments))
			self.write("SUCCESS")
		else:
			self.write("NO SOCKET")

class AddCard(tornado.web.RequestHandler):
	def post(self):
		imgId = ''
		if (self.request.files):
			file_body = self.request.files['image'][0]['body']
			img = Image.open(StringIO.StringIO(file_body))
			imgId = "./static/"+str(uuid.uuid4())+"."+img.format
			img.save(imgId, img.format)

		message = self.get_argument("message")
		if (self.get_argument("type") == "video"):
			ytid = message.split('?v=')[1]
			message = "<iframe width='400' height='300' src='//www.youtube.com/embed/"
			message += ytid
			message += "?autoplay=1' frameborder='0' allowfullscreen></iframe>"

		newCard = {}
		newCard["type"] = self.get_argument("type")
		newCard["src"] = "." + imgId
		newCard["name"] = self.get_argument("name")
		newCard["message"] = message
		newCard["sender"] = self.get_argument("sender")
		newCard["id"] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))
		stack.append(newCard);

		self.redirect("../contribute/index.html");

# Communicates with the projector HTML5 screen
class ProjectorWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
    	global ProjSocket
    	ProjSocket = self
        print "Opened socket to Projector"

    def on_message(self, message):
        self.write_message(u'{"connected": true}')

    def on_close(self):
        print "WebSocket closed"