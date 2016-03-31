import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
import time
import serial
import os

define("server-port", default = 8000, help = "Starts the server on the given port", type = int)
define("statics-root", default = "statics/")
define("templates-root", default = "templates/")

class SerialMonitorApplication(tornado.web.Application):
	def __init__(self):
		handlers=[
			(r"/", IndexController),
			(r"/statics/(.*)", tornado.web.StaticFileHandler, {'path': options.statics-root}),
			(r"/serial/data-monitor", SerialDataSocket)
		]
		
		settings = dict(
			app_title = u"Serial Monitor Application",
			template_path = os.path.join(os.path.dirname(__file__), options.templates-root[:1]),
			statics_path = os.path.join(os.path.dirname(__file__), options.statics-root[:1]),
		)
		
		super(SerialMonitorApplication, self).__init__(handlers, **settings)
		
class IndexController(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')
 
class SerialDataSocket(tornado.websocket.WebSocketHandler):
	clients = []

	def open(self):
		print 'New connection - %s' % self
		self.clients.append(self)
		self.write_message('Connected to SerialData Socket')

	def on_message(self, msg):
		print 'Received: %s' % msg
		self.write_message('Received: %s' % msg)

	def on_close(self):
		print 'Closed - %s' % self
		self.clients.remove(self)

		
def main():
	tornado.options.parse_command_line()
	httpServer = tornado.httpserver.HTTPServer(SerialMonitorApplication())
	httpServer.listen(options.server-port)

	# Print so we know the server started
	print "Listening on port:", options.port

	# Start the application on the main IO loop
	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()
