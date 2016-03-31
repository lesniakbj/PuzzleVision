import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
import tornado.options

import controllers
import config


tornado.options.define("server-port", default = 8000, help = "Starts the server on the given port", type = int)
tornado.options.define("statics-root", default = configs.Routes.STATICS_ROOT)
tornado.options.define("templates-root", default = configs.Routes.TEMPLATES_ROOT)


class SerialMonitorApplication(tornado.web.Application):
	def __init__(self):
		handlers = [
			(config.Routes.ROOT, controllers.HomeController),
			(r"/serial", SerialChatController),
			(r"/serial/data-monitor", SerialDataSocket),
			(r"/statics/(.*)", tornado.web.StaticFileHandler, {'path': tornado.options.statics-root})
		]
		
		settings = dict(
			app_title = u"Serial Monitor Application",
			template_path = os.path.join(os.path.dirname(__file__), tornado.options.templates-root[:-1]),
			statics_path = os.path.join(os.path.dirname(__file__), tornado.options.statics-root[:-1]),
		)
		
		super(SerialMonitorApplication, self).__init__(handlers, **settings)


class SerialChatController(tornado.web.RequestHandler):
	def get(self):
		self.render('serial-chat.html')


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
	httpServer.listen(tornado.options.server-port)

	# Print so we know the server started
	print "Listening on port:", tornado.options.port

	# Start the application on the main IO loop
	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()

