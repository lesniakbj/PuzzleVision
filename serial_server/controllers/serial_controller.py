import tornado.web


class SerialComController(tornado.web.RequestHandler):
    def get(self):
        self.render('serial-monitor.html')