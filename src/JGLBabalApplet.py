from StringIO import StringIO
from java import awt, applet
from java.net import URL
from JGLBabalCanvas import JGLBabalCanvas


class JGLBabalApplet(applet.Applet):

    def _get_map_file(self):
        map_param = self.getParameter('map')
        map_url = URL(self.getDocumentBase(), map_param)
        self.showStatus('Loading ' + map_url.toString())
        map_is = map_url.openStream()
        map_buf = ""
        i = map_is.read()
        while i != -1:
            map_buf = map_buf + chr(i)
            i = map_is.read()
        return StringIO(map_buf)

    def init(self):
        map_file = self._get_map_file()
        size = self.getSize()
        self.canvas = JGLBabalCanvas(size.width, size.height, map_file)

        def status_callback(status, self=self):
            self.showStatus(status)
        self.canvas.game.status_callback = status_callback

        self.add(self.canvas)
        
    def start(self):
        self.canvas.start()

    def stop(self):
        self.canvas.stop()
