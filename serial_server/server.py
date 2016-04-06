"""
Puzzle Vision Serial Server:
The puzzle vision serial server is meant to collect data from
the serial ports and allow communication to the attached device
from a web site. This will allow us to view the data that is being
transmitted from the AStar32u4, which includes system status,
collected video, and motor data.

The server will allow commands to be sent to the AStar32u4 so that
the system can be configured in the desired manner. Finally, the
server will also show the status of I/O pins on the RPi, and will
act as a general I/O monitor.
"""
import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen

from tornado.options import define, options
from controllers import home_controller, serial_controller
from serial_com import serial_socket, serial_com
from config import strings, server, serial, routes


define("server_port", default=server.PORT,
                      help=strings.HELP_SERVER_PORT, type=int)
define("serial_port", default=serial.PORT,
                      help=strings.HELP_SERIAL_PORT, type=int)
define("statics_root", default=routes.STATICS_ROOT,
                       help=strings.HELP_STATICS, type=str)
define("templates_root", default=routes.TEMPLATES_ROOT,
                         help=strings.HELP_TEMPLATES, type=str)

statics_root = routes.STATICS_ROOT
templates_root = routes.TEMPLATES_ROOT
server_port = server.PORT

class SerialMonitorApplication(tornado.web.Application):
    controllers = []
    settings = []

    serialPort = None

    def __init__(self):
        self.initSerialPort()
        self.initControllers()
        self.initSettings()

        super(SerialMonitorApplication, self).__init__(self.controllers,
                                                       **self.settings)

    def initControllers(self):
        self.controllers = [
            (routes.ROOT, home_controller.HomeController),
            (routes.SERIAL_MONITOR, serial_controller.SerialComController),
            (routes.SERIAL_SOCKET, serial_socket.SerialMonitorSocket, dict(serial=self.serialPort)),
            (
                routes.STATICS_PATTERN,
                tornado.web.StaticFileHandler,
                {
                    'path': statics_root
                }
            )
        ]

    def initSettings(self):
        self.settings = dict(
            app_title=u"Serial Monitor Application",
            #default_handler_class=error_controller.ErrorController,
            template_path=os.path.join(
                os.path.dirname(__file__),
                templates_root[:-1]
            ),
            statics_path=os.path.join(
                     os.path.dirname(__file__),
                statics_root[:-1]
            )
        )

    def initSerialPort(self):
        self.serialPort = serial_com.SerialCom()
        self.serialPort.daemon = True
        self.serialPort.start()

def main():
    tornado.options.parse_command_line()
    httpServer = tornado.httpserver.HTTPServer(SerialMonitorApplication())
    httpServer.listen(server_port)

    # Print so we know the server started
    print('Listening on port:', server_port)

    # Start the application on the main IO loop
	# Add a callback that will be called periodically to check
	# the serial port for data.
    iol = tornado.ioloop.IOLoop.instance()
    iol.start()


if __name__ == "__main__":
    main()
