import tornado.websocket


class SerialMonitorSocket(tornado.websocket.WebSocketHandler):
    connections = []

    def open(self):
        print('New connection - %s' % self)
        self.connections.append(self)
        self.write_message('Connected to Serial Monitor Socket')

    def on_message(self, msg):
        print('Received: %s', msg)
        self.write_message('Received: %s' % msg)

    def on_close(self):
        print('Closed - ', self)
        self.connections.remove(self)