import tornado.web
import tornado.

# Communicates with the projector HTML5 screen
class ProjectorWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
    	ProjSocket = self
        print "Opened socket to Projector"

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print "WebSocket closed"